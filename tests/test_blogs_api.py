import requests
import time
from test_auth_api import decorator_printing_tests_names
from flaskr.models import Post


@decorator_printing_tests_names
def test_get_all_posts():
    resp = requests.get(
        url="http://127.0.0.1:5000/api/blog",
    )
    print(resp.json())


@decorator_printing_tests_names
def test_create_new_post():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]

    data = {"title": "Hello REST", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/create",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


@decorator_printing_tests_names
def test_update_post_with_timeout(sleep_duration=1):
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]
    time.sleep(sleep_duration)
    data = {"title": "updated Hello REST", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/update/3",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


@decorator_printing_tests_names
def test_update_post_with_logout():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = {"title": "updated Hello REST", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/update/3",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


@decorator_printing_tests_names
def test_delete_post_by_id(post_id):

    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )

    token = resp.json()["auth_token"]
    resp = requests.delete(
        url=f"http://127.0.0.1:5000/api/blog/delete/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(resp.json())


if __name__ == "__main__":
    test_delete_post_by_id(1)

