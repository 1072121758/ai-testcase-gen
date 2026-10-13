

def test_get_current_user(client, token):

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == "wendi"