# Todo API 接口文档

一个基于 FastAPI 的学习项目：用户登录（JWT 认证）+ Todo 业务。

- Base URL：`http://127.0.0.1:8000`
- 交互式文档（Swagger UI）：`http://127.0.0.1:8000/docs`
- 测试账号：`wendi` / `123456`

## 启动方式

```powershell
uv run uvicorn app.main:app --reload
```

## 认证说明

除登录接口外，所有接口都需要在请求头携带 JWT Token：

```
Authorization: Bearer <access_token>
```

认证流程：

```
客户端                          服务端
  |                               |
  |-- POST /login (用户名密码) -->|
  |<-- access_token (JWT) -------|
  |                               |
  |-- GET /todos                 |
  |   Authorization: Bearer xxx >|-- 验证 Token
  |<-- 业务数据 ------------------|
```

- 签名算法：HS256
- 有效期：30 分钟（过期后返回 401，需重新登录）
- Token 载荷：`sub`（用户名）、`exp`（过期时间）

## 接口总览

| 方法   | 路径          | 说明             | 是否需要 Token |
| ------ | ------------- | ---------------- | -------------- |
| POST   | /login        | JSON 登录        | 否             |
| POST   | /auth/token   | 表单登录（OAuth2） | 否             |
| GET    | /users/me     | 获取当前用户信息 | 是             |
| POST   | /todos        | 创建 Todo        | 是             |
| GET    | /todos        | 查询 Todo 列表   | 是             |
| GET    | /             | 健康检查         | 否             |

---

## 1. JSON 登录

`POST /login`

按项目接口设计文档定义的 JSON 格式登录。

**请求体（application/json）**

```json
{
    "username": "wendi",
    "password": "123456"
}
```

**成功响应 200**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

**错误响应**

| 状态码 | 场景               | 响应体                                    |
| ------ | ------------------ | ----------------------------------------- |
| 401    | 用户名或密码错误   | `{"detail": "用户名或密码错误"}`          |
| 422    | 缺少 username/password | `{"detail": [...]}`（FastAPI 校验错误） |

**示例（curl）**

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "wendi", "password": "123456"}'
```

---

## 2. 表单登录（OAuth2 标准）

`POST /auth/token`

与 `/login` 逻辑完全相同，区别是使用表单格式。Swagger 的 Authorize 弹窗、以及标准 OAuth2 客户端走这个端点。

**请求体（application/x-www-form-urlencoded）**

```
username=wendi&password=123456
```

**成功响应 200**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

**错误响应**：同 `/login`（401 / 422）。

**示例（curl）**

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -d "username=wendi" \
  -d "password=123456"
```

---

## 3. 获取当前用户信息

`GET /users/me`

**请求头**

```
Authorization: Bearer <access_token>
```

**成功响应 200**

```json
{
    "username": "wendi",
    "email": "wendi@example.com"
}
```

**错误响应**

| 状态码 | 场景           | 响应体                            |
| ------ | -------------- | --------------------------------- |
| 401    | 未携带 Token   | `{"detail": "Not authenticated"}` |
| 401    | Token 无效     | `{"detail": "无效 Token"}`        |
| 401    | Token 已过期   | `{"detail": "Token 已过期"}`      |

**示例（curl）**

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 4. 创建 Todo

`POST /todos`

**请求头**

```
Authorization: Bearer <access_token>
```

**请求体（application/json）**

```json
{
    "title": "学习pytest"
}
```

**成功响应 201**

```json
{
    "id": 1,
    "title": "学习pytest",
    "status": "created"
}
```

**错误响应**

| 状态码 | 场景         | 响应体                            |
| ------ | ------------ | --------------------------------- |
| 401    | 未携带/无效 Token | `{"detail": "..."}`          |
| 422    | 缺少 title   | `{"detail": [...]}`               |

**示例（curl）**

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "学习pytest"}'
```

---

## 5. 查询 Todo 列表

`GET /todos`

**请求头**

```
Authorization: Bearer <access_token>
```

**成功响应 200**

```json
[
    {
        "id": 1,
        "title": "学习pytest"
    }
]
```

**错误响应**：同 `GET /users/me`（未携带/无效/过期 Token 均为 401）。

**示例（curl）**

```bash
curl http://127.0.0.1:8000/todos \
  -H "Authorization: Bearer <access_token>"
```

---

## 6. 健康检查

`GET /`

**成功响应 200**

```json
{
    "message": "Welcome to Todo API"
}
```

---

## 错误码汇总

| 状态码 | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| 200    | 成功                                                         |
| 201    | 创建成功（仅 POST /todos）                                   |
| 401    | 认证失败：未携带 Token、Token 无效/过期、用户名或密码错误    |
| 422    | 请求参数校验失败：缺少必填字段或字段类型错误                 |

所有错误响应统一为 FastAPI 默认格式：`{"detail": "错误描述"}`。

## 数据存储说明

当前为学习项目，用户和 Todo 数据保存在内存中（重启服务即清空），后续可替换为 SQLite/MySQL 等真实数据库。

## 运行测试

```powershell
uv run pytest tests/ -v
```

共 10 个用例，覆盖登录、Token 校验、Todo 增查的完整链路。
