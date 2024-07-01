from contextlib import asynccontextmanager
import sqlite3
from dataclasses import dataclass
import sqlite3
from pydantic import BaseModel
from typing import Optional
import sqlalchemy
from sqlalchemy import Engine
from uvicorn import run
import os
from typing import Annotated
from fastapi import FastAPI, Request, Response, HTTPException, Header, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from datetime import datetime
import secrets
from .db import db as tables
from sqlmodel import SQLModel, and_, create_engine, Session, delete, select, or_

origins = [
    "http://localhost",
    "http://localhost:8007",
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

db: Engine
TOKEN_LENGTH = 128


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db

    db_path = "friend_finder.db"
    if "DATABASE_FILE" in os.environ:
        db_path = os.environ["DATABASE_FILE"]

    sqlite_url = f"sqlite:///{db_path}"

    db = create_engine(sqlite_url, echo=True)

    # Create all tables
    SQLModel.metadata.create_all(db)

    yield


app = FastAPI(lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home_page():
    return "Hello..!!"


class RegisterBody(BaseModel):
    username: str
    email: str
    password: str
    pincode: int
    topics: str


class LoginResponse(BaseModel):
    session_token: str
    id: int
    username: str


@app.post("/register")
async def register_root(body: RegisterBody, request: Request) -> LoginResponse:
    topics = [(topic.lower()).strip() for topic in body.topics.split(",")]

    pass_hashed = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    with Session(db) as session:
        user = tables.User(
            username=body.username,
            email=body.email,
            password=pass_hashed,
            pincode=body.pincode,
        )
        session.add(user)
        session.commit()

        if len(topics) > 0:
            await insert_user_topics(session, user, topics)

        token = secrets.token_urlsafe(TOKEN_LENGTH)
        session.add(tables.Session(user_id=user.id, token=token))
        session.commit()

        return LoginResponse(
            session_token=token,
            id=user.id,
            username=user.username,
        )


class LoginBody(BaseModel):
    email: str
    password: str


#  Login User by using email or password
@app.post("/login")
async def login_root(body: LoginBody, response: Response) -> LoginResponse:
    with Session(db) as session:
        stmt = select(tables.User).where(tables.User.email == body.email).limit(1)
        user = session.exec(stmt).one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email")

        if not bcrypt.checkpw(
            body.password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )

        token = secrets.token_urlsafe(TOKEN_LENGTH)
        session.add(tables.Session(user_id=user.id, token=token))

        session.commit()

        return LoginResponse(session_token=token, id=user.id, username=user.username)


@dataclass
class LoggedInUser:
    user: tables.User
    session: tables.Session


async def get_current_user(
    authorization: Annotated[str, Header()],
) -> LoggedInUser:
    with Session(db) as session:
        stmt = (
            select(tables.User, tables.Session)
            .where(
                tables.User.id == tables.Session.user_id,
                tables.Session.token == authorization,
            )
            .limit(1)
        )
        result = session.exec(stmt).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
            )
        user, session = result
        return LoggedInUser(user, session)


class UserInformation(BaseModel):
    """
    Same as tables.User but without the password
    """

    id: int
    username: str
    email: str
    pincode: int
    name: Optional[str] = None
    number: Optional[str] = None
    address: Optional[str] = None
    joined_on: str

    @classmethod
    def from_user(cls, user: tables.User) -> "UserInformation":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            pincode=user.pincode,
            name=user.name,
            number=user.number,
            address=user.address,
            joined_on=user.joined_on,
        )


#  Check the user is loge in or not
@app.get("/logged_in/")
async def logged_in(
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
) -> UserInformation:
    return UserInformation.from_user(current_user.user)


#  Logout user
@app.post("/logout/")
async def logout(current_user: Annotated[LoggedInUser, Depends(get_current_user)]):
    with Session(db) as session:
        session.delete(current_user.session)
        session.commit()


class UserWithTopics(BaseModel):
    user: UserInformation
    topics: list[tables.Topic]


@app.get("/suggestion")
async def suggestion(
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
) -> list[UserWithTopics]:
    with Session(db) as session:
        stmt = select(tables.UserTopic).where(
            tables.UserTopic.user_id == current_user.user.id
        )
        user_topics = session.exec(stmt).fetchall()
        topic_ids = [u.topic_id for u in user_topics]

        stmt = select(tables.User, tables.UserTopic, tables.Topic).where(
            # JOIN
            tables.UserTopic.user_id == tables.User.id,
            tables.UserTopic.topic_id == tables.Topic.id,
            tables.User.pincode == current_user.user.pincode,
            tables.User.id != current_user.user.id,
        )
        stmt = stmt.where(or_(*[tables.Topic.id == id for id in topic_ids]))

        result = session.exec(stmt).fetchall()

        user_id_to_suggestion: dict[int, UserWithTopics] = {}

        for user, _, topic in result:
            if user.id not in user_id_to_suggestion:
                user_id_to_suggestion[user.id] = UserWithTopics(
                    user=UserInformation.from_user(user), topics=[topic]
                )
            else:
                user_id_to_suggestion[user.id].topics.append(topic)

        return list(user_id_to_suggestion.values())


# # Data of the user whose profile is  checked out ( current user)

# # A user Profile data....


@app.get("/user_profile/{username}")
async def user_profile(
    username: str,
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
) -> UserWithTopics:
    with Session(db) as session:
        return get_user_with_topics(session, username=username)


@app.get("/profile/")
async def profile(current_user: Annotated[LoggedInUser, Depends(get_current_user)]):
    with Session(db) as session:
        return get_user_with_topics(session, username=current_user.user.username)


class AddFriend(BaseModel):
    user_id: int


# TODO: reject, if already sent friend request.
@app.post("/add_friend/")
async def add_friend(
    body: AddFriend,
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
):
    with Session(db) as session:
        stmt = select(tables.User).where(tables.User.id == body.user_id)
        friend_user = session.exec(stmt).one_or_none()
        if friend_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User ID does not exist"
            )

        session.add(
            tables.FriendRequest(
                sender=current_user.user.id,
                reciever=friend_user.id,
            )
        )
        session.commit()


# #  get data of friend list which shows on sidebar of the messenger...


@app.get("/get_inbox_users/")
async def get_inbox_users(
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
) -> list[UserWithTopics]:
    with Session(db) as session:
        # Get all friends added by current user
        stmt = select(tables.FriendRequest).where(
            tables.FriendRequest.sender == current_user.user.id,
        )
        friend_requests = session.exec(stmt).fetchall()

        inbox_user_ids = set([fr.reciever for fr in friend_requests])

        # Get all users who have exchanged atleast one message
        # with user
        stmt = select(tables.Message).where(
            or_(
                tables.Message.sender == current_user.user.id,
                tables.Message.reciever == current_user.user.id,
            )
        )
        messages = session.exec(stmt).fetchall()

        # Merge them
        for message in messages:
            inbox_user_ids.add(message.sender)
            inbox_user_ids.add(message.reciever)

        # Remove current user's ID
        if current_user.user.id in inbox_user_ids:
            inbox_user_ids.remove(current_user.user.id)

        inbox_users: list[UserWithTopics] = []

        for id in inbox_user_ids:
            inbox_users.append(get_user_with_topics(session, user_id=id))
        return inbox_users


class SendMessageBody(BaseModel):
    message: str


@app.post("/send_message/{user_id}")
async def message_set(
    body: SendMessageBody,
    user_id: int,
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
):
    with Session(db) as session:
        session.add(
            tables.Message(
                sender=current_user.user.id, reciever=user_id, content=body.message
            )
        )
        session.commit()


@app.get("/get_message/{user_id}")
async def get_message(
    user_id: int,
    current_user: Annotated[LoggedInUser, Depends(get_current_user)],
) -> list[tables.Message]:
    with Session(db) as session:
        stmt = select(tables.Message).where(
            or_(
                and_(
                    tables.Message.sender == user_id,
                    tables.Message.reciever == current_user.user.id,
                ),
                and_(
                    tables.Message.sender == current_user.user.id,
                    tables.Message.reciever == user_id,
                ),
            )
        )
        return sorted(
            session.exec(stmt).fetchall(),
            key=lambda x: x.sent_at,
            reverse=True,
        )


# # store messages


async def insert_user_topics(
    session: Session, user: tables.User, topic_names: list[str]
):
    for topic_name in topic_names:
        stmt = select(tables.Topic).where(tables.Topic.name == topic_name)
        result = session.exec(stmt).fetchall()

        if len(result) == 0:
            topic = tables.Topic(name=topic_name)
            session.add(topic)
            session.commit()
            topic_id = topic.id
        else:
            topic_id = result[0].id

        session.add(tables.UserTopic(topic_id=topic_id, user_id=user.id))
    session.commit()


def get_user_with_topics(
    session: Session, *, username: str | None = None, user_id: int | None = None
) -> UserWithTopics:
    if user_id is None and username is None:
        raise Exception("Atleast one of 'user_id' or 'username' is required")

    if username is not None:
        stmt = select(tables.User).where(tables.User.username == username)
    else:
        stmt = select(tables.User).where(tables.User.id == user_id)
    user = session.exec(stmt).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user."
        )

    stmt = select(tables.Topic, tables.UserTopic).where(
        # Topic + topicusername
        tables.Topic.id == tables.UserTopic.topic_id,
        # user + topicusername
        tables.UserTopic.user_id == user.id,
    )
    topics = session.exec(stmt).fetchall()
    return UserWithTopics(
        user=UserInformation.from_user(user), topics=[t for t, _ in topics]
    )


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
