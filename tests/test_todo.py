def test_create_todo(client, auth_headers):

    response = client.post(
        "/todos",
        headers=auth_headers,
        json={
            "title": "学习pytest"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "学习pytest"

    assert data["status"] == "created"


def test_list_todos(client, auth_headers):

    response = client.get(
        "/todos",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 0

