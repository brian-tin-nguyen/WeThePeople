from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve files from the /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- Endpoint ----------------
@app.get("/")
def root():
    return {"message": "WeThePeople is running!"}