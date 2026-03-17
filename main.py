from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Brian",
        "title": "FastAPI is Awesome",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed libero nec tortor tincidunt semper sit amet vitae urna. Mauris at tincidunt orci.",
        "date_posted": "October 1, 2025",
    },
    {
        "id": 2,
        "author": "Tina",
        "title": "Python is super duper Awesome",
        "content": "Nullam euismod aliquet nibh in porttitor. Etiam tincidunt sapien pharetra euismod posuere. Integer leo mauris, luctus in ullamcorper a, molestie sit amet ipsum. Pellentesque ac magna lectus.",
        "date_posted": "October 21, 2025",
    },
]

# endpoint
@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "title": "Home"},)

# endpoint 2
@app.get("/api/posts")
def get_posts():
    return posts

# endpoint 3: get a single specfic post 
@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# endpoint 4: post.html
@app.get("/post/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse("post.html", {"request": request, "post": post, "title": title})
    raise HTTPException(status_code=404, detail="Post not found")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )