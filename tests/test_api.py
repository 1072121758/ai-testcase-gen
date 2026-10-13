from fastapi.testclient import TestClient





# def login_token(username: str = "wendi", password: str = "123456") -> str:
#     resp = client.post("/login", json={"username": username, "password": password})
#     assert resp.status_code == 200, resp.text
#     return resp.json()["access_token"]


# def test_root():
#     resp = client.get("/")
#     assert resp.status_code == 200


# def test_login_returns_token():
#     resp = client.post("/login", json={"username": "wendi", "password": "123456"})
#     data = resp.json()
#     assert resp.status_code == 200
#     assert data["token_type"] == "bearer"
#     assert data["access_token"]


# def test_login_wrong_password():
#     resp = client.post("/login", json={"username": "wendi", "password": "wrong"})
#     assert resp.status_code == 401


# def test_auth_token_form_login():
#     # Swagger 的 Authorize 弹窗用表单格式登录
#     resp = client.post(
#         "/auth/token",
#         data={"username": "wendi", "password": "123456"},
#     )
#     data = resp.json()
#     assert resp.status_code == 200
#     assert data["token_type"] == "bearer"
#     assert data["access_token"]


# def test_users_me_requires_token():
#     resp = client.get("/users/me")
#     assert resp.status_code == 401


# def test_users_me_with_token():
#     token = login_token()
#     resp = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
#     assert resp.status_code == 200
#     assert resp.json() == {"username": "wendi", "email": "wendi@example.com"}


# def test_users_me_with_invalid_token():
#     resp = client.get("/users/me", headers={"Authorization": "Bearer not-a-jwt"})
#     assert resp.status_code == 401


# def test_create_todo():
#     token = login_token()
#     resp = client.post(
#         "/todos",
#         json={"title": "学习pytest"},
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     data = resp.json()
#     assert resp.status_code == 201
#     assert data["title"] == "学习pytest"
#     assert data["status"] == "created"
#     assert "id" in data


# def test_list_todos():
#     token = login_token()
#     headers = {"Authorization": f"Bearer {token}"}
#     client.post("/todos", json={"title": "学习pytest"}, headers=headers)
#     resp = client.get("/todos", headers=headers)
#     assert resp.status_code == 200
#     titles = [todo["title"] for todo in resp.json()]
#     assert "学习pytest" in titles


# def test_todos_requires_token():
#     resp = client.get("/todos")
#     assert resp.status_code == 401
