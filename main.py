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
   mycursor = conex.mydb.cursor()
   mycursor.execute(f"SELECT * FROM login WHERE colaborador = '{username}' and senha = '{password}' ")
   myresult = mycursor.fetchall()
   for lgn in myresult:
    try:
      if lgn[1] == username and lgn[2] == password:
          mycursor = conex.mydb.cursor()
          mycursor.execute(f"SELECT * FROM login")
          myresult = mycursor.fetchall()
          return templates.TemplateResponse("usuarios.html", {"request": request, "users": myresult})
    except:
        return templates.TemplateResponse("index.html", {"request": request})


@app.get("/usuarios", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request" : request})


@app.get("/aviso", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("aviso.html", {"request" : request})


if __name__ == '__mail__':
    app.rum()