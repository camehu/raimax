from fastapi import FastAPI, Request, requests, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import conex


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request" : request})


@app.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
   ''' mycursor = conex.mydb.cursor()
    sql = "SELECT * FROM login WHERE colaborador = username and senha = password"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult == 1:
        return templates.TemplateResponse("login.html", {"request" : request , "login": 1})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "login": 0})'''


if __name__ == '__mail__':
    app.rum()