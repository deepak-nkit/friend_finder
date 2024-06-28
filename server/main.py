from contextlib import asynccontextmanager
from dataclasses import dataclass
import sqlite3
from pydantic import BaseModel
from uvicorn import run
import os
from typing import Annotated
from fastapi import FastAPI, Request, Response, HTTPException, Header, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from datetime import datetime
import secrets


origins = [
    "http://localhost",
    "http://localhost:8007",
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
con: sqlite3.Connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    global con
    global data
    global cur

    db_path = "friend_finder.db"

    if "DATABASE_FILE" in os.environ:
        db_path = os.environ['DATABASE_FILE']

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # date = datetime

    cur.execute("""
            CREATE TABLE IF NOT EXISTS user(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT UNIQUE,
                    Email VARCHAR(255) NOT NULL UNIQUE, 
                    Password TEXT,
                    pincode INTEGER NOT NULL,
                    Name Text,
                    Number TEXT  UNIQUE,
                    Address TEXT,
                    JoinedOn DATE
            );   
         """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS topic( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER ,  
                TopicName VARCHAR(100) NOT NULL,
                FOREIGN KEY(User_id) REFERENCES user(id)
                
             );             
         """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS session(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        User_id INTEGER,
                        Token TEXT NOT NULL UNIQUE,
                        FOREIGN KEY(User_id) REFERENCES user(id)
                       
                );
          """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS message(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        From_userid INTEGER,
                        To_userid INTEGER,
                        Sent_at DATE,
                        FOREIGN KEY(From_userid) REFERENCES user(id)
                       
                );
          """)

    data = con.execute("SELECT * FROM user")
    data = data.fetchall()
    print("Total users:", len(data))
    yield


app = FastAPI(lifespan=lifespan, debug=True)
# app = FastAPI()

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


@app.post("/register")
async def register_root(body: RegisterBody, request: Request):
    username = body.username
    password = body.password
    email = body.email
    pincode = body.pincode  # topic = data["topics"]
    topics = [topic.strip() for topic in body.topics.split(",")]
    pass_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    User_id = 0
    try:
        cur.execute(
            """
                    INSERT INTO user (Username , Email , Password , Pincode , JoinedOn) VALUES (?, ? ,?,?,?)
                    """,
            (username, email, pass_hashed, pincode, current_datetime),
        )
        con.commit()
        cur.execute(
            "SELECT  id FROM user  WHERE Email = ?",
            (email,),
        )

        row = cur.fetchone()
        User_id = row[0]
        if len(topics) > 0:
            var1 = """ INSERT INTO topic (User_id , TopicName) VALUES (?, ?)"""
            for topic in topics:
                cur.execute(var1, (User_id, topic))
                con.commit()

        con.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            raise HTTPException(
                status_code=400, detail="Email or Username already |||||  registered"
            )
    token = secrets.token_urlsafe(16)
    cur.execute(
        """
                INSERT INTO session (User_id , Token) VALUES (? ,?)
                """,
        (User_id, token),
    )
    con.commit()
    return {
        "session_token": token,
        "id": User_id,
        "username": username,
    }


class LoginBody(BaseModel):
    email: str
    password: str


#  Login User by using email or password


@app.post("/login")
async def login_root(body: LoginBody, response: Response):
    email = body.email
    password = body.password
    cur.execute("SELECT id, username, Password FROM user WHERE email = ?", (email,))
    row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    id, username, hashed_password = row

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = secrets.token_urlsafe(16)
    cur.execute(
        """
                INSERT INTO session (User_id , Token) VALUES (? ,?)
                """,
        (id, token),
    )
    con.commit()

    return {
        "session_token": token,
        "id": id,
        "username": username,
    }


class User:
    def __init__(
        self, user_id: int, email: str, username: str, pincode: int, token: str
    ) -> None:
        self.username = username
        self.user_id = user_id
        self.email = email
        self.pincode = pincode
        self.session_token = token


async def get_current_user(
    authorization: Annotated[str, Header()],
) -> User:
    print("----****---***----***---", authorization)
    token = authorization
    cur.execute(
        "SELECT  user.Username , user.Email,  user.Pincode, session.User_id  FROM session JOIN user ON user.id = session.User_id WHERE session.Token = ?",
        (token,),
    )
    row = cur.fetchone()
    if row != None:
        user = User(
            username=row[0],
            email=row[1],
            pincode=row[2],
            user_id=row[3],
            token=token,
        )
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="NOT Authorized Please Login First!",
        )


#  Check the user is loge in or not


@app.get("/loged_in/")
async def loged_in(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "user_id": current_user.user_id,
    }


#  Logout user


@app.post("/logout/")
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    print("*****logout")
    cur.execute("DELETE FROM session WHERE token = ?;", (current_user.session_token,))
    con.commit()
    return current_user.session_token


# select the topic , and other information of the Other users in same area.....


def get_user(user_id: int) -> dict:
    cur.execute(
        """
                SELECT username , JoinedOn FROM user WHERE id = ? 
            """,
        (user_id,),
    )
    test = cur.fetchone()
    joined_date = datetime.strptime(test[1], "%Y-%m-%d %H:%M:%S")
    days_ago = (datetime.now() - joined_date).days
    cur.execute(
        """
                SELECT TopicName FROM topic WHERE User_id = ? 
            """,
        (user_id,),
    )
    row = cur.fetchall()
    dic = {"username": test[0], "days_ago": days_ago, "topic": row}
    return dic


#  Suggestion root to show the data to user at Home page

# @dataclass
# class Item:
#     username: str
#     topic:list
#     day_ago: int


@app.get("/suggestion")
async def suggestion(
    current_user: Annotated[User, Depends(get_current_user)],
    # authorization: Annotated[str, Header()],
):
    # Select the User Id's which has the  same topic...
    cur.execute(
        """
            SELECT DISTINCT User_id from topic where Topicname IN (SELECT TopicName from topic WHERE User_id = ?) AND User_id != (?)
        """,
        (
            current_user.user_id,
            current_user.user_id,
        ),
    )
    user_ids = cur.fetchall()
    sug = []

    for id in user_ids:
        sug.append(get_user(id[0]))
    return {"suggestion": sug}


# Data of the user whose profile is  checked out ( current user)
# class Profilebody(BaseModel):
#     username: str

# A user Profile data....


@app.get("/user_profile/{username}")
async def user_profile(
    username: str,
    current_user: Annotated[User, Depends(get_current_user)],
):
    print()
    print(username)
    print()
    cur.execute(
        """
            SELECT user.id , user.Name , user.email , user.Pincode , user.Joinedon , user.Address , topic.User_id  FROM  user JOIN topic ON topic.User_id = user.id WHERE user.Username = (?)
        """,
        (username,),
    )
    row = cur.fetchone()
    cur.execute(
        """
            SELECT TopicName  FROM topic WHERE User_id = (?)
        """,
        (row[6],),
    )
    topic = cur.fetchall()
    profile_user_data = {
        "username": username,
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "pincode": row[3],
        "days_ago": row[4],
        "address": row[5],
        "user_id": row[6],
        "topics": topic,
    }
    print(profile_user_data)
    return profile_user_data


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
