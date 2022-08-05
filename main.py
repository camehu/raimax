from fastapi import FastAPI, Request, requests, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from hash_token import hash, blacklist, token
import conex

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# ROTAS PARA INSERIR, EDITAR E DELETAR USUARIOS

@app.get("/teste", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("teste.html", {"request": request, "teste": 0})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/suporte-interno", response_class=HTMLResponse)
async def root(request: Request):
    mycursor = conex.mydb.cursor()
    mycursor.execute("SELECT * FROM aviso")
    myresult = mycursor.fetchall()
    return templates.TemplateResponse("suporte-interno.html", {"request": request, "aviso": myresult})


@app.get("/listaviso", response_class=HTMLResponse)
async def listaviso(request: Request):
    mycursor = conex.mydb.cursor()
    mycursor.execute("SELECT * FROM aviso")
    myresult = mycursor.fetchall()
    return templates.TemplateResponse("listaviso.html", {"request": request, "aviso": myresult})


@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request):
    mycursor = conex.mydb.cursor()
    mycursor.execute("SELECT * FROM login")
    myresult = mycursor.fetchall()
    return templates.TemplateResponse("usuarios.html", {"request": request, "login": myresult})


@app.get("/painel", response_class=HTMLResponse)
async def painel(request: Request):
    tkn = blacklist.blacklist
    for tk in tkn:
        if len(tk) == 0:
            return templates.TemplateResponse("index.html", {"request": request})
        else:
            return templates.TemplateResponse("painel.html", {"request": request})


@app.post("/validacpanel")
async def validacpanel(request: Request, username: str = Form(), password: str = Form(), ):
    mycursor = conex.mydb.cursor()
    mycursor.execute(f"SELECT * FROM login WHERE nickname ='{username}' ")
    myresult = mycursor.fetchall()

    lista = len(myresult)
    if lista == 0:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        for nome in myresult:
            if nome[3] == username:
                senha = hash.verifcar_hask(password, nome[2])
                if senha:
                    blacklist.blacklist.append(token.token(nome[0], nome[1], [3]))
                    return templates.TemplateResponse("painel.html", {"request": request})
                else:
                    return RedirectResponse(url="/", status_code=303, )
            else:
                return templates.TemplateResponse("index.html", {"request": request})


@app.post("/inserir")
async def inserir(request: Request, username: str = Form(), password: str = Form(), nickname: str = Form(),
                  tipo: str = Form()):
    mycursor = conex.mydb.cursor()
    cript_senha = hash.gerar_hash(password)
    sql = f"INSERT INTO `login`(`colaborador`, `senha`, `nickname`, `tipo`) VALUES (%s, %s, %s, %s)"
    val = (username, cript_senha, nickname, tipo)
    mycursor.execute(sql, val)
    conex.mydb.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


@app.post("/editar", response_class=HTMLResponse)
async def editar(request: Request, id: str = Form(), username: str = Form(), password: str = Form(),
                 nickname: str = Form(), tipo: str = Form()):
    mycursor = conex.mydb.cursor()
    cript_senha = hash.gerar_hash(password)
    sql = f"UPDATE `login` SET `id`='{id}',`colaborador`='{username}',`senha`='{cript_senha}',`nickname`='{nickname}',`tipo`='{tipo}' WHERE id = '{id}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


@app.post("/deletar", response_class=HTMLResponse)
async def deletar(request: Request, idaviso: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"DELETE FROM login WHERE id = '{idaviso}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return RedirectResponse(url=f"usuarios", status_code=303)


# ROTAS PARA INSERIR, EDITAR E DELETAR AVISOS

@app.get("/aviso", response_class=HTMLResponse)
async def aviso(request: Request):
    try:
        mycursor = conex.mydb.cursor()
        mycursor.execute("SELECT * FROM aviso")
        myresult = mycursor.fetchall()
        return templates.TemplateResponse("aviso.html", {"request": request, "aviso": myresult})

    except:
        templates.TemplateResponse("index.html", {"request": request})


@app.post("/cad_aviso")
async def cad_aviso(request: Request, data: str = Form(), problema: str = Form(), descricao: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"INSERT INTO `aviso`(`data`, `problema`, `descricao`) VALUES (%s, %s, %s)"
    val = (data, problema, descricao)
    mycursor.execute(sql, val)
    conex.mydb.commit()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/edit_aviso", response_class=HTMLResponse)
async def edit_aviso(request: Request, idaviso: str = Form(), data_aviso: str = Form(), problema: str = Form(),
                     descricao: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"UPDATE `aviso` SET `idaviso`='{idaviso}',`data`='{data_aviso}',`problema`='{problema}',`descricao`='{descricao}' WHERE id = '{idaviso}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/del_aviso", response_class=HTMLResponse)
async def del_aviso(request: Request, idaviso: str = Form()):
    mycursor = conex.mydb.cursor()
    sql = f"DELETE FROM aviso WHERE idaviso = '{idaviso}'"
    mycursor.execute(sql)
    conex.mydb.commit()
    return RedirectResponse(url=f"aviso", status_code=303)


if __name__ == '__mail__':
    app.rum()
