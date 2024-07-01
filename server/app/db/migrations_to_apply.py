from databases import Database
from .migration import MigrationFunction

"""
NOTE: DO NOT EDIT EXISTING MIGRATIONS. IT WILL BREAK THE DATABASE.
Create a new function and add migration there, and append it to `MIGRATIONS` variable list at the end.
"""

async def migration_01(db: Database):
    await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE, 
                    password TEXT NOT NULL,
                    pincode INTEGER NOT NULL,
                    name TEXT,
                    number TEXT UNIQUE,
                    address TEXT,
                    joined_on DATE NOT NULL
            );   
         """)

    await db.execute("""
            CREATE TABLE IF NOT EXISTS topics ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
             );             
         """)

    await db.execute("""
            CREATE TABLE IF NOT EXISTS user_topics ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
                FOREIGN KEY(topic_id) REFERENCES topics(id)

             );             
         """)

    await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        token TEXT NOT NULL UNIQUE,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                );
          """)

    await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender INTEGER NOT NULL,
                        reciever INTEGER NOT NULL,
                        sent_at DATE NOT NULL,
                        content TEXT NOT NULL,
                        FOREIGN KEY(sender) REFERENCES users(id)
                        FOREIGN KEY(reciever) REFERENCES users(id)
                );
          """)

    await db.execute("""
                CREATE TABLE IF NOT EXISTS friend_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender INTEGER NOT NULL,
                        reciever INTEGER NOT NULL,
                        FOREIGN KEY(sender) REFERENCES users(id)
                        FOREIGN KEY(reciever) REFERENCES users(id)
                );
          """)


MIGRATIONS: list[MigrationFunction] = [migration_01]
