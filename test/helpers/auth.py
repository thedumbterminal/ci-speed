from main import app
import json


def auth_get_request(token, url):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.get(
            url,
            headers={
                "Authentication-Token": token,
                "accept": "application/json",
            },
        )
        print(response)
        print(response.status_code)
        return json.loads(response.data)


def auth_post_request(token, url, data):
    with app.test_request_context(), app.test_client() as test_client:
        response = test_client.post(
            url,
            headers={
                "Authentication-Token": token,
                "accept": "application/json",
            },
            data=data,
        )
        print(response.status_code)
        return json.loads(response.data)
