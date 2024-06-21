from contextlib import asynccontextmanager
import sqlite3
from pydantic import BaseModel
from uvicorn import run
from typing import Annotated
from fastapi import FastAPI, Request, Response, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from datetime import datetime
import secrets


origins = [
    "http://localhost",
    "http://localhost:8007",
    "http://localhost:5500",
]
con: sqlite3.Connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    global con
    global data
    global cur

    con = sqlite3.connect("friend_finder.db")
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

    # except sqlite3.OperationalError as e:
    #     if "already exists" in str(e):
    #             print("\nThe table is already exist Skip the Creating Step: \n")
    #     else:
    #          raise e
    data = con.execute("SELECT * FROM user")
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

# app.mount("/my_other_files", StaticFiles(directory="/web"), name="template")

# template = Jinja2Templates(directory="/web/template")


# def hashed_password(password):
#     password_byte = password.encode("utf-8")
#     salt = bcrypt.gensalt()
#     hashed_pass = bcrypt.hashpw(password_byte , salt)
#     return hashed_pass
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
    pass_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
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


@app.post("/login")
async def login_root(body: LoginBody, response: Response):
    email = body.email
    password = body.password
    var1 = "SELECT Password FROM user WHERE email = ?"
    var2 = (email,)
    cur.execute("SELECT id , Username , Password FROM user WHERE email = ?", (email,))
    test = cur.fetchone()
    id = test[0]
    username = test[1]
    if test is None:
        raise HTTPException(status_code=400, detail="Invalid email or Password")
    else:
        check = cur.execute(var1, var2)
        if check is None:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        hashed_password = check.fetchone()[0]
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token = secrets.token_urlsafe(16)
        cur.execute(
            """
                    INSERT INTO session (User_id , Token) VALUES (? ,?)
                    """,
            (id, token),
        )
        return {
            "session_token": token,
            "id": id,
            "username": username,
        }


class User:
    def __init__(self, user_id: int, email: str, username: str, token: str) -> None:
        self.username = username
        self.user_id = user_id
        self.email = email
        self.session_token = token


async def get_current_user(
    # authorization: Annotated[str, Header(convert_underscores=False)],) -> User:
    authorization: Annotated[str, Header()],
) -> User:
    print("------------------------", authorization)
    token = authorization
    cur.execute(
        "SELECT  user.Username , user.Email, session.User_id FROM session JOIN user ON user.id = session.User_id WHERE session.Token = ?",
        (token,),
    )
    row = cur.fetchone()
    if row != None:
        user = User(
            user_id=row["User_id"],
            username=row["Username"],
            email=row["Email"],
            token=token,
        )
        return user
    else:
        raise HTTPException(status_code=401, detail="Login First")


@app.get("/loged_in/")
async def loged_in(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user.user_id


@app.post("/logout/")
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    cur.execute("DELETE FROM session WHERE token = ?;", current_user.session_token)
    return current_user.session_token


# @app.post
if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
