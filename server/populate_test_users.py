import httpx
import time
import os
import asyncio

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


async def make_user(client: httpx.Client, username: str, pincode: int, topics: list[str]):
    start = time.time()
    response = client.post(
        BACKEND_URL + "/register",
        json={
            "username": username,
            "email": username + "@g.com",
            "pincode": pincode,
            "password": username,
            "topics": topics,
        },
    )
    time_taken = time.time() - start
    response.raise_for_status()
    print(f"Created {username=} {pincode=} {topics=} in {time_taken}s")

async def main():
    with httpx.Client() as client:
        await make_user(client, "kiki", 111111, ['coding', 'gaming'])
        await make_user(client, "alice", 111111, ['coding'])
        await make_user(client, "totoro", 111111, ['python', 'gaming'])
        await make_user(client, "heron", 111111, ['python', 'coding', 'gaming'])
        await make_user(client, "thor", 111111, ['python', 'coding', 'gaming'])
        await make_user(client, "shifu", 111111, ['python', 'coding', 'gaming'])
        await make_user(client, "crane", 111111, ['python', 'coding', 'gaming'])
        await make_user(client, "bob", 222222, ['python', 'gaming'])
        await make_user(client, "po", 111111, ['java'])
  


if __name__ == "__main__":
    asyncio.run(main())
