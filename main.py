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


@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request):
        mycursor = conex.mydb.cursor()
        mycursor.execute("SELECT * FROM login")
        myresult = mycursor.fetchall()
        return templates.TemplateResponse("inserir.html", {"request": request, "login": myresult})


@app.get("/painel", response_class=HTMLResponse)
async def painel(request: Request):
    return templates.TemplateResponse("painel.html", {"request": request})


@app.get("/aviso", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("aviso.html", {"request" : request})


@app.get("/listaaviso", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("listaaviso.html", {"request" : request})


@app.get("/listaviso", response_class=HTMLResponse)
async def usuarios(request: Request):
        mycursor = conex.mydb.cursor()
        mycursor.execute("SELECT * FROM aviso")
        myresult = mycursor.fetchall()
        return templates.TemplateResponse("aviso.html", {"request": request, "aviso": myresult})


@app.post("/validacpanel")
async def login(request: Request, username: str = Form(), password: str = Form()):
    mycursor = conex.mydb.cursor()
    mycursor.execute(f"SELECT * FROM login WHERE colaborador ='{username}' AND senha = '{password}' ")
    myresult = mycursor.fetchall()
    if myresult is not None:
        return templates.TemplateResponse("painel.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})


@app.post("/inserir", response_class=HTMLResponse)
async def inserir(request: Request, username: str = Form(), password: str = Form(), nickname: str = Form(), tipo: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"INSERT INTO `login`(`colaborador`, `senha`, `nickname`, `tipo`) VALUES (%s, %s, %s, %s)"
    val = (username, password, nickname, tipo)
    mycursor.execute(sql, val)
    conex.mydb.commit()
    return templates.TemplateResponse("inserir.html", {"request": request, "USER": mycursor.rowcount})


@app.post("/editar", response_class=HTMLResponse)
async def editar(request: Request, id: str = Form(), username: str = Form(), password: str = Form(), nickname: str = Form(), tipo: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"UPDATE `login` SET `id`='{id}',`colaborador`='{username}',`senha`='{password}',`nickname`='{nickname}',`tipo`='{tipo}' WHERE id = '{id}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return templates.TemplateResponse("inserir.html", {"request": request, "editado": mycursor.rowcount})


@app.post("/deletar", response_class=HTMLResponse)
async def deletar(request: Request, id: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"DELETE FROM login WHERE id = '{id}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return templates.TemplateResponse("inserir.html", {"request": request, "deletado": mycursor.rowcount})


if __name__ == '__mail__':
    app.rum()