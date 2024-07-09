import asyncio
from collections import defaultdict
from contextlib import asynccontextmanager
import sqlite3
from typing import DefaultDict, Literal
from dataclasses import dataclass
import sqlite3
from pydantic import UUID4, BaseModel
from typing import Optional
import uuid
import sqlalchemy
from sqlalchemy import Engine, text
import sqlalchemy.exc
from uvicorn import run
import os
from typing import Annotated
from fastapi import FastAPI, Request, Response, HTTPException, Header, Depends, status
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from datetime import datetime
import secrets
from .db import db as tables
from sqlmodel import SQLModel, and_, update, create_engine, Session, delete, select, or_
from sqlalchemy import text


origins = [
    "http://localhost",
    "http://localhost:8007",
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

db: Engine
TOKEN_LENGTH = 128


class TimeoutException(Exception): ...


Key = tuple[int, int]
MessageQueue = asyncio.Queue[tables.Message]


class MessageQueueHandler:
    def __init__(self):
        self.queues: DefaultDict[Key, set[MessageQueue]] = defaultdict(set)

        # {[q1, (u1, u2)], [q2, (u3, u1)]}
        self.deleted_queues: set[tuple[Key, MessageQueue]] = set()

    # /send_message
    def broadcast_message(self, key: Key, message: tables.Message):
        for queue in self.queues[key]:
            queue.put_nowait(message)

        # Not thread safe
        for k, queue in self.deleted_queues:
            self.queues[k].remove(queue)

        self.deleted_queues.clear()

    async def wait_for_message(
        self, key: Key, timeout: int = 60
    ) -> tables.Message | None:
        queue = asyncio.Queue()
        self.queues[key].add(queue)

        done, _ = await asyncio.wait(
            [asyncio.create_task(queue.get())], timeout=timeout
        )
        self.deleted_queues.add((key, queue))

        if len(done) == 0:
            return None

        return await list(done)[0]


message_handler = MessageQueueHandler()


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
    topics: list[str]


class LoginResponse(BaseModel):
    session_token: str
    id: int
    username: str


class RegisterUniqueError(BaseModel):
    message: str
    unique_field: Literal["email"] | Literal["username"]


@app.post(
    "/register",
    responses={409: {"model": RegisterUniqueError}},
)
async def register(body: RegisterBody, request: Request) -> LoginResponse:
    topics = [topic.lower().strip() for topic in body.topics]
    topics = [topic for topic in topics if len(topic) != 0]

    pass_hashed = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    with Session(db) as session:  # BEGIN TRANSACTION
        user = tables.User(
            username=body.username,
            email=body.email,
            password=pass_hashed,
            pincode=body.pincode,
        )
        try:
            session.add(user)
            session.flush()
        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed: user.email" in str(e):
                # TODO: openapi types seem wrong here?
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=RegisterUniqueError(
                        message="email already exists", unique_field="email"
                    ).model_dump(),
                )

            if "UNIQUE constraint failed: user.username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=RegisterUniqueError(
                        message="username already exists", unique_field="username"
                    ).model_dump(),
                )
            print(e)
            raise Exception("Couldn't match email/username for Integrity Error")

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
async def login(body: LoginBody, response: Response) -> LoginResponse:
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


async def get_logged_in_user(
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
    name: Optional[str]
    number: Optional[str]
    address: Optional[str]
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
@app.get("/get_current_user/")
async def get_current_user(
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> UserInformation:
    return UserInformation.from_user(current_user.user)


#  Logout user
@app.post("/logout/")
async def logout(current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)]):
    with Session(db) as session:
        session.delete(current_user.session)
        session.commit()


class UserWithTopics(BaseModel):
    user: UserInformation
    topics: list[tables.Topic]
    is_friend: bool


@app.get("/suggestion")
async def suggestion(
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> list[UserWithTopics]:
    with Session(db) as session:
        stmt = select(tables.UserTopic).where(
            tables.UserTopic.user_id == current_user.user.id
        )
        user_topics = session.exec(stmt).fetchall()
        topic_ids = [u.topic_id for u in user_topics]

        if len(topic_ids) == 0:
            return []

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
                    user=UserInformation.from_user(user),
                    topics=[topic],
                    is_friend=is_friend(session, current_user.user.id, user.id),
                )
            else:
                user_id_to_suggestion[user.id].topics.append(topic)

        return list(user_id_to_suggestion.values())


# # Data of the user whose profile is  checked out ( current user)

# # A user Profile data....


@app.get("/user_profile/{username}")
async def user_profile(
    username: str,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> UserWithTopics:
    with Session(db) as session:
        return get_user_with_topics(session, current_user.user.id, username=username)


@app.get("/user_profile")
async def self_user_profile(
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> UserWithTopics:
    with Session(db) as session:
        return get_user_with_topics(
            session, current_user.user.id, username=current_user.user.username
        )


class AddFriend(BaseModel):
    user_id: int


# TODO: reject, if already sent friend request.
@app.post("/add_friend/")
async def add_friend(
    body: AddFriend,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
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
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
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
            inbox_users.append(
                get_user_with_topics(session, current_user.user.id, user_id=id)
            )
        return inbox_users


class SendMessageBody(BaseModel):
    message: str
    client_id: UUID4


@app.post("/send_message/{username}")
async def send_message(
    body: SendMessageBody,
    username: str,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> tables.Message:
    with Session(db) as session:
        user = get_user_with_topics(session, current_user.user.id, username=username)
        message = tables.Message(
            sender=current_user.user.id,
            reciever=user.user.id,
            content=body.message,
            client_id=str(body.client_id),
        )
        session.add(message)
        session.commit()

        message_handler.broadcast_message((message.sender, message.reciever), message)
        message_handler.broadcast_message((message.reciever, message.sender), message)

        return message


@app.get("/get_messages/{username}")
async def get_messages(
    username: str,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
    limit: int = 20,
    before_id: Optional[int] = None,
) -> list[tables.Message]:
    with Session(db) as session:
        user = get_user_with_topics(session, current_user.user.id, username=username)

        stmt = select(tables.Message).where(
            or_(
                and_(
                    tables.Message.sender == user.user.id,
                    tables.Message.reciever == current_user.user.id,
                ),
                and_(
                    tables.Message.sender == current_user.user.id,
                    tables.Message.reciever == user.user.id,
                ),
            )
        )
        if before_id is not None:
            stmt = stmt.where(tables.Message.id < before_id)

        stmt = stmt.order_by(text("id DESC")).limit(limit)

        return list(session.exec(stmt).fetchall())


@app.get("/poll_message/{username}")
async def poll_message(
    username: str,
    after_id: int,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
    limit: int = 20,
) -> list[tables.Message]:
    with Session(db) as session:
        user = get_user_with_topics(session, current_user.user.id, username=username)
        key = (current_user.user.id, user.user.id)
        task = asyncio.create_task(message_handler.wait_for_message(key))
        stmt = select(tables.Message).where(
            or_(
                and_(
                    tables.Message.sender == user.user.id,
                    tables.Message.reciever == current_user.user.id,
                ),
                and_(
                    tables.Message.sender == current_user.user.id,
                    tables.Message.reciever == user.user.id,
                ),
            )
        )
        stmt = stmt.where(tables.Message.id > after_id)

        stmt = stmt.order_by(text("id ASC")).limit(limit)
        messages = session.exec(stmt).fetchall()
    # await asyncio.sleep(5) # for test

    if len(messages) != 0:
        task.cancel()
        return list(messages)
    else:
        message = await task
        if message is None:
            return []
        else:
            return [message]


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
            session.flush()
            topic_id = topic.id
        else:
            topic_id = result[0].id

        session.add(tables.UserTopic(topic_id=topic_id, user_id=user.id))
    session.flush()


def get_user_with_topics(
    session: Session,
    current_user_id: int,
    *,
    username: str | None = None,
    user_id: int | None = None,
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
        user=UserInformation.from_user(user),
        topics=[t for t, _ in topics],
        is_friend=is_friend(session, current_user_id, user.id),
    )


def is_friend(session: Session, user1_id: int, user2_id: int):
    stmt = select(tables.FriendRequest).where(
        or_(
            and_(
                tables.FriendRequest.sender == user1_id,
                tables.FriendRequest.reciever == user2_id,
            ),
            and_(
                tables.FriendRequest.sender == user2_id,
                tables.FriendRequest.reciever == user1_id,
            ),
        )
    )
    return session.exec(stmt).one_or_none() is not None


class SearchBody(BaseModel):
    username: str


class SearchResponse(BaseModel):
    users: list[UserInformation]


@app.get("/search_user")
async def search_user(
    body: SearchBody,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
) -> SearchResponse:
    users: list[UserInformation] = []
    with Session(db) as session:
        stmt = select(tables.User).where(
            text("username like :search_query").bindparams(
                search_query="%" + body.username + "%"
            )
        )
        user = session.exec(stmt).fetchall()
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid Username")
        for u in user:
            users.append(UserInformation.from_user(u))
        print(users)
        return SearchResponse(users=users)


class EditBody(BaseModel):
    username: str
    email: str
    name: str
    address: str
    latitude: float
    longitude: float
    topics: list[str]


@app.post("/edit")
async def edit(
    body: EditBody,
    current_user: Annotated[LoggedInUser, Depends(get_logged_in_user)],
    request: Request,
):
    topics = [topic.lower().strip() for topic in body.topics]
    topics = [topic for topic in topics if len(topic) != 0]

    print("------------------", body.latitude, body.longitude)

    with Session(db) as session:  # BEGIN TRANSACTION
        try:
            update_user_info(
                current_user.user.id,
                body.name,
                body.username,
                body.email,
                body.address,
                body.latitude,
                body.longitude,
            )

            # if len(topics) > 0:
            #     await insert_user_topics(session, user, topics)

        except sqlalchemy.exc.IntegrityError as e:
            if "UNIQUE constraint failed: user.email" in str(e):
                # TODO: openapi types seem wrong here?
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=RegisterUniqueError(
                        message="email already exists", unique_field="email"
                    ).model_dump(),
                )

            if "UNIQUE constraint failed: user.username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=RegisterUniqueError(
                        message="username already exists", unique_field="username"
                    ).model_dump(),
                )
            print(e)
            raise Exception("Couldn't match email/username for Integrity Error")


def update_user_info(
    id: int,
    name: str,
    new_username: str,
    new_email: str,
    address: str,
    lat: float,
    lng: float,
):
    with Session(db) as session:
        statement = select(tables.User).where(tables.User.id == id)
        results = session.exec(statement)
        info = results.one()
        print("-----------------ifo", info)
        info.name = name
        info.username = new_username
        info.email = new_email
        info.address = address
        info.latitude = lat
        info.longitude = lng
        session.add(info)


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
