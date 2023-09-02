import requests


def test_register_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/register",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    print(resp.json())


def test_register_with_invalid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/register",
        json={"username": "joe@gmail.com", "passwrd": "123456"},
    )
    print(resp.json())


if __name__ == "__main__":
    test_register_with_valid_data()
