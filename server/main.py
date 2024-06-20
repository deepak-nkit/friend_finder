from contextlib import asynccontextmanager
import sqlite3
from uvicorn import run
from typing import Annotated
from fastapi import FastAPI, Request, Response, HTTPException, Header ,Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import secrets


origins = [
    "http://localhost",
    "http://localhost:8007",
    "http://localhost:5500",
]

# last_time = None
# test = 0
con: sqlite3.Connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    global con
    global data
    global cur

    con = sqlite3.connect("finder.db")
    cur = con.cursor()
    # date = datetime
    print("==================== table1")

    cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT UNIQUE,
                    Email VARCHAR(255) NOT NULL UNIQUE, 
                    Password TEXT,
                    pincode INTEGER,
                    Name Text,
                    Number TEXT  UNIQUE,
                    Address TEXT 
            );       """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS topic( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER ,  
                TopicName VARCHAR(100) NOT NULL,
                FOREIGN KEY(user_data) REFERENCES user_data(id)
                
         );             
         """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS session(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        User_id INTEGER,
                        Token TEXT NOT NULL UNIQUE
                        FOREIGN KEY(user_data) REFERENCES user_data(id)
                       
                );
            """)

    print("==================== table")

    # except sqlite3.OperationalError as e:
    #     if "already exists" in str(e):
    #             print("\nThe table is already exist Skip the Creating Step: \n")
    #     else:
    #          raise e
    data = con.execute("SELECT * FROM user_data")
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


@app.post("/register")
async def register_root(request: Request, data: dict):
    username = data["username"]
    password = data["password"]
    email = data["email"]
    pass_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        cur.execute(
            """
                    INSERT INTO user_data (Username , Email , Password) VALUES (? , ? ,?)
                    """,
            (username, email, pass_hashed),
        )
        con.commit()
    except sqlite3.IntegrityError:
        print("from here ")
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"Message: User register Successfully"}


@app.post("/login")
async def read_root(data: dict, response: Response):
    email = data["email"]
    password = data["password"]
    var1 = "SELECT Password FROM user_data WHERE email = ?"
    var2 = (email,)
    cur.execute("SELECT id , Password FROM user_data WHERE email = ?", (email,))
    test = cur.fetchone()
    print("========================================", test["user_id"])
    if test is None:
        raise HTTPException(status_code=400, detail="Invalid email")
    else:
        check = cur.execute(var1, var2)
        if check is None:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        hashed_password = check.fetchone()[0]

        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token = secrets.token_urlsafe(16)

        print("token  ----------------- ", token)
        cur.execute(
            """
                    INSERT INTO session (User_id , Token) VALUES (? ,?)
                    """,
            (test["id"], token),
        )
        response.set_cookie(
            key="session_token", value=token, max_age=3600 * 24 * 365 * 200
        )
        print(
            "---------------------------------------------------------------------------------------",
            response,
        )

        return {"message": "Login successful"}


class User:
    def __init__(self, user_id:int ,  email:str , username:str , token:str ) -> None:
        self.username = username
        self.user_id = user_id
        self.email = email
        self.session_token =  token     
    


async def get_current_user(authorization: Annotated[str, Header(convert_underscores=False)],) ->User:

    token = authorization.split(" ")[1]
    cur.execute("SELECT  user_data.Username , user_data.Email, session.User_id FROM session JOIN user_data ON user_data.id = session.User_id WHERE session.Token = ?", (token,))
    row = cur.fetchone()
    if(row != None):
        user = User (
            user_id = row['User_id'],
            username = row['Username'],
            email=row['Email'],
            token = token,
        )
        return user
    else:
        raise HTTPException(status_code=401, detail="Login First")    


@app.get("/loged_in/")
async def loged_in(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user.user_id

@app.get("/logout/")
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    cur.execute("DELETE FROM session WHERE token = ?;",current_user.session_token)
    return current_user.session_token


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8006)
