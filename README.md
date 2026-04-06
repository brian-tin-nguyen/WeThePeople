# WeThePeople API

A Reddit-style REST API built with FastAPI and Python.

## Tech Stack
- FastAPI
- SQLAlchemy + SQLite
- JWT Authentication (python-jose)
- Pydantic
- Bcrypt password hashing

## Setup
1. Clone the repo
2. Install dependencies: `uv sync`
3. Create a `.env` file with `SECRET_KEY=yoursecretkey`
4. Run: `fastapi dev main.py`
5. Visit: `http://127.0.0.1:8000/docs`

## Endpoints
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /users/register | No | Create account |
| POST | /users/login | No | Get JWT token |
| GET | /posts/ | No | Get all posts |
| GET | /posts/{id} | No | Get one post |
| POST | /posts/ | Yes | Create a post |
| DELETE | /posts/{id} | Yes | Delete your post |
