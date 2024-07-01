from fastapi.testclient import TestClient
from .main import app
import random


def test_sanity():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


last_user_id = 0


def create_user(client: TestClient, pincode: int, topics: str):
    global last_user_id

    last_user_id += 1
    username = f"user-{last_user_id}"
    # Create user
    response = client.post(
        "/register",
        json={
            "username": username,
            "password": username,
            "email": username + "@email.com",
            "pincode": pincode,
            "topics": topics,
        },
    )
    assert response.status_code == 200
    data = response.json()
    return {"username": username, "token": data["session_token"], "id": data["id"]}


def test_suggestion():
    with TestClient(app) as client:
        user1 = create_user(client, 1, "coding, gaming")
        user2 = create_user(client, 1, "coding, python")
        user3 = create_user(client, 2, "coding, python")
        user4 = create_user(client, 2, "java")
        print(user1, user2)

        # Test user 1 suggestion
        response = client.get("/suggestion", headers={"authorization": user1["token"]})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["user"]["username"] == user2["username"]

        # Test user 2 suggestion
        response = client.get("/suggestion", headers={"Authorization": user2["token"]})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["user"]["username"] == user1["username"]

        # Test user 3 suggestion
        response = client.get("/suggestion", headers={"Authorization": user3["token"]})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 0

        # Test user 4 suggestion
        response = client.get("/suggestion", headers={"Authorization": user4["token"]})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 0


def test_user_profile():
    with TestClient(app) as client:
        user1 = create_user(client, 1, "python")
        user2 = create_user(client, 1, "coding, gaming")

        response = client.get(
            f"/user_profile/{user2['username']}",
            headers={"authorization": user1["token"]},
        )
        assert response.status_code == 200
        data = response.json()

        assert data["user"]["username"] == user2["username"]
        assert len(data["topics"]) == 2

        topic_names = [t["name"] for t in data["topics"]]
        assert sorted(topic_names) == ["coding", "gaming"]


def test_self_profile():
    with TestClient(app) as client:
        user1 = create_user(client, 1, "python")
        user2 = create_user(client, 1, "coding, gaming")

        response = client.get(
            f"/profile/",
            headers={"authorization": user1["token"]},
        )
        assert response.status_code == 200
        data = response.json()

        assert data["user"]["username"] == user1["username"]
        assert len(data["topics"]) == 1

        topic_names = [t["name"] for t in data["topics"]]
        assert sorted(topic_names) == ["python"]


def test_get_inbox_users():
    with TestClient(app) as client:
        user1 = create_user(client, 1, "python")
        # friend_request: user1 -> user2
        user2 = create_user(client, 1, "coding, gaming")
        # friend_request: user3 -> user1
        user3 = create_user(client, 1, "gaming")
        # message: user4 -> user1
        user4 = create_user(client, 1, "java")
        # message: user1 -> user5
        user5 = create_user(client, 1, "java")
        # friend_request+message: user6 -> user1
        user6 = create_user(client, 1, "java")
        # nothing
        user7 = create_user(client, 1, "java")

        response = client.post(
            f"/add_friend/",
            headers={"authorization": user1["token"]},
            json={"user_id": user2["id"]},
        )
        assert response.status_code == 200
        response = client.post(
            f"/add_friend/",
            headers={"authorization": user3["token"]},
            json={"user_id": user1["id"]},
        )
        assert response.status_code == 200

        response = client.post(
            f"/send_message/{user1['id']}",
            headers={"authorization": user4["token"]},
            json={"message": "Yes"},
        )
        assert response.status_code == 200

        response = client.post(
            f"/send_message/{user5['id']}",
            headers={"authorization": user1["token"]},
            json={"message": "Yes"},
        )
        assert response.status_code == 200

        response = client.post(
            f"/send_message/{user1['id']}",
            headers={"authorization": user6["token"]},
            json={"message": "Yes"},
        )
        assert response.status_code == 200

        response = client.post(
            f"/add_friend/",
            headers={"authorization": user1["token"]},
            json={"user_id": user6["id"]},
        )
        assert response.status_code == 200

        response = client.get(
            f"/get_inbox_users/",
            headers={"authorization": user1["token"]},
        )
        assert response.status_code == 200
        data = response.json()

        friend_ids = [t["user"]["id"] for t in data]
        assert sorted(friend_ids) == sorted(
            [
                user2["id"],
                user4["id"],
                user5["id"],
                user6["id"],
            ]
        )

def test_get_message():
    with TestClient(app) as client:
        user1 = create_user(client, 1, "python")
        user2 = create_user(client, 1, "coding, gaming")

        response = client.post(
            f"/send_message/{user1['id']}",
            headers={"authorization": user2["token"]},
            json={"message": "one"},
        )
        assert response.status_code == 200
        response = client.post(
            f"/send_message/{user1['id']}",
            headers={"authorization": user2["token"]},
            json={"message": "two"},
        )
        assert response.status_code == 200
        response = client.post(
            f"/send_message/{user2['id']}",
            headers={"authorization": user1["token"]},
            json={"message": "three"},
        )
        assert response.status_code == 200
        
        response = client.get(
            f"/get_message/{user2['id']}/",
            headers={"authorization": user1["token"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        assert data[0]['sender'] == user1['id']
        assert data[0]['reciever'] == user2['id']
        assert data[0]['content'] == 'three'

        assert data[1]['sender'] == user2['id']
        assert data[1]['reciever'] == user1['id']
        assert data[1]['content'] == 'two'

        assert data[2]['sender'] == user2['id']
        assert data[2]['reciever'] == user1['id']
        assert data[2]['content'] == 'one'

