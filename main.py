from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


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