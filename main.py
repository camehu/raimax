from fastapi import FastAPI, Request, requests, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request" : request})


@app.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    return templates.TemplateResponse("aviso.html", {"request" : request , "username": username})


if __name__ == '__mail__':
    app.rum()