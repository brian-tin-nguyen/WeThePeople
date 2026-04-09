from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import users, posts

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(posts.router)

# Home
@app.get("/")
def root():
    return FileResponse("templates/index.html")

# Login
@app.get("/login")
def login_page():
    return FileResponse("templates/login.html")

# Register
@app.get("/register")
def register_page():
    return FileResponse("templates/register.html")

# Admin 
@app.get("/admin")
def admin_page():
    return FileResponse("templates/admin.html")

# Individual post page
@app.get("/post/{post_id}")
def post_page(post_id: int):
    return FileResponse("templates/post.html")

# Edit the individual post page
@app.get("/edit/{post_id}")
def edit_page(post_id: int):
    return FileResponse("templates/edit.html")