from fastapi import FastAPI, Request, requests, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import hash_token.hash
import sqlAlchemy_db

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# TELA USUARIOS

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/new_layout", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("new_layout.html", {"request": request})


@app.get("/painel", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("painel.html", {"request": request})


@app.post("/validacpanel")
async def validacpanel(request: Request, username: str = Form(), password: str = Form(), ):
    admin_user = sqlAlchemy_db.session.query(sqlAlchemy_db.User).filter(
        sqlAlchemy_db.User.apelido == f'{username}').one()
    very_pass = hash_token.hash.verifcar_hask(password, admin_user.senha)
    if very_pass:
        return RedirectResponse(url=f"painel", status_code=303)
    else:
        return RedirectResponse(url=f"/", status_code=303)


@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request):
    query = sqlAlchemy_db.session.query(sqlAlchemy_db.User).all()
    return templates.TemplateResponse("usuarios.html", {"request": request, "login": query})


@app.post("/inserir")
async def inserir(username: str = Form(), nickname: str = Form(), password: str = Form(),
                  tipo: str = Form()):
    pass_hash = hash_token.hash.gerar_hash(password)
    user = sqlAlchemy_db.User(usuario=f'{username}', apelido=f'{nickname}', senha=f'{pass_hash}', tipo=f'{tipo}')
    sqlAlchemy_db.session.add(user)
    sqlAlchemy_db.session.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


@app.post("/deletar", response_class=HTMLResponse)
async def deletar(request: Request, iduser: str = Form()):
    del_user = sqlAlchemy_db.session.query(sqlAlchemy_db.User).filter(sqlAlchemy_db.User.idsuario == f'{iduser}').one()
    sqlAlchemy_db.session.delete(del_user)
    sqlAlchemy_db.session.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


@app.post("/editar", response_class=HTMLResponse)
async def editar(request: Request, id: str = Form(), username: str = Form(), nickname: str = Form(),
                 password: str = Form(),
                 tipo: str = Form()):
    pass_hash = hash_token.hash.gerar_hash(password)
    admin_user = sqlAlchemy_db.session.query(sqlAlchemy_db.User).filter(sqlAlchemy_db.User.idsuario == f'{id}').one()
    admin_user.usuario = username
    admin_user.apelido = nickname
    admin_user.senha = pass_hash
    admin_user.tipo = tipo
    sqlAlchemy_db.session.add(admin_user)
    sqlAlchemy_db.session.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


# TELE AVISOS

@app.get("/aviso", response_class=HTMLResponse)
async def aviso(request: Request):
    query = sqlAlchemy_db.session.query(sqlAlchemy_db.Aviso).all()
    return templates.TemplateResponse("aviso.html", {"request": request, "aviso": query})


@app.post("/cad_aviso")
async def cad_aviso(request: Request, data: str = Form(), problema: str = Form(), descricao: str = Form()):
    aviso = sqlAlchemy_db.Aviso(data=f'{data}', problema=f'{problema}', descricao=f'{descricao}')
    sqlAlchemy_db.session.add(aviso)
    sqlAlchemy_db.session.commit()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/del_aviso", response_class=HTMLResponse)
async def del_aviso(request: Request, idaviso: str = Form()):
    aviso = sqlAlchemy_db.session.query(sqlAlchemy_db.Aviso).filter(sqlAlchemy_db.Aviso.idaviso == f'{idaviso}').one()
    sqlAlchemy_db.session.delete(aviso)
    sqlAlchemy_db.session.commit()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/edit_aviso", response_class=HTMLResponse)
async def edit_aviso(request: Request, data_aviso: str = Form(), problema: str = Form(),
                     descricao: str = Form()):
    aviso = sqlAlchemy_db.Aviso(data=f'{data_aviso}', problema=f'{problema}', descricao=f'{descricao}')
    sqlAlchemy_db.session.add(aviso)
    sqlAlchemy_db.session.commit()

    return RedirectResponse(url=f"aviso", status_code=303)


@app.get("/listaviso", response_class=HTMLResponse)
async def listaviso(request: Request):
    query = sqlAlchemy_db.session.query(sqlAlchemy_db.Aviso).all()
    return templates.TemplateResponse("listaviso.html", {"request": request, "aviso": query})


if __name__ == '__mail__':
    app.rum()
