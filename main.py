import mysql
from fastapi import FastAPI, Request, requests, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import conex
import hash_token.hash

app = FastAPI()

templates = Jinja2Templates( directory="templates" )

app.mount( "/static", StaticFiles( directory="static" ), name="static" )


# TELA USUARIOS

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/validacpanel")
async def validacpanel(request: Request, username: str = Form(), password: str = Form(), ):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = "SELECT nickname, senha FROM `login` WHERE nickname = '{username}'"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    cursor.close()
    conex.mydb.close()
    for usr in myresult:
        very_pass = hash_token.hash.verifcar_hask(password, usr[1])
        if very_pass:
            return RedirectResponse( url=f"usuarios", status_code=303 )
        else:
            return RedirectResponse( url=f"/", status_code=303 )


@app.get( "/usuarios", response_class=HTMLResponse )
async def usuarios(request: Request):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = "SELECT * FROM login"
    cursor.execute( sql )
    myresult = cursor.fetchall()
    cursor.close()
    conex.mydb.close()
    return templates.TemplateResponse( "usuarios.html", {"request": request, "login": myresult} )


@app.post( "/inserir" )
async def inserir(username: str = Form(), nickname: str = Form(), password: str = Form(),
                  tipo: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    cript_senha = hash_token.hash.gerar_hash( password )
    sql = "INSERT INTO `login`(`colaborador`, `nickname`, `senha`, `tipo`) VALUES (%s, %s, %s, %s)"
    val = (username, nickname, cript_senha, tipo)
    cursor.execute( sql, val )
    cursor.close()
    conex.mydb.close()
    return RedirectResponse( url=f"usuarios", status_code=303 )


@app.post( "/deletar", response_class=HTMLResponse )
async def deletar(request: Request, idaviso: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = "DELETE FROM login WHERE idlogin = '{idaviso}'"
    cursor.execute( sql )
    cursor.close()
    cursor.close()
    conex.mydb.close()
    return RedirectResponse( url=f"usuarios", status_code=303 )


@app.post( "/editar", response_class=HTMLResponse )
async def editar(request: Request, id: str = Form(), username: str = Form(), password: str = Form(),
                 nickname: str = Form(), tipo: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    cript_senha = hash_token.hash.gerar_hash( password )
    sql = "UPDATE `login` SET `colaborador`='{username}',`nickname`='{nickname}', `senha`='{cript_senha}' ,`tipo`='{tipo}' WHERE idlogin = '{id}'"
    cursor.execute( sql )
    cursor.close()
    conex.mydb.close()
    return RedirectResponse( url=f"usuarios", status_code=303 )


# TELE AVISOS

@app.get("/aviso", response_class=HTMLResponse )
async def aviso(request: Request):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = f"SELECT * FROM aviso"
    cursor.execute( sql )
    myresult = cursor.fetchall()
    cursor.close()
    conex.mydb.close()
    return templates.TemplateResponse( "aviso.html", {"request": request, "aviso": myresult} )


@app.post("/cad_aviso")
async def cad_aviso(request: Request, data: str = Form(), problema: str = Form(), descricao: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = "INSERT INTO `aviso`(`data`, `problema`, `descricao`) VALUES (%s, %s, %s)"
    val = (data, problema, descricao)
    cursor.execute(sql, val)
    cursor.close()
    conex.mydb.close()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/del_aviso", response_class=HTMLResponse)
async def del_aviso(request: Request, idaviso: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = f"DELETE FROM aviso WHERE idaviso = '{idaviso}'"
    cursor.execute(sql)
    cursor.close()
    conex.mydb.close()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.post("/edit_aviso", response_class=HTMLResponse)
async def edit_aviso(request: Request, idaviso: str = Form(), data_aviso: str = Form(), problema: str = Form(),
                     descricao: str = Form()):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = f"UPDATE `aviso` SET `data`='{data_aviso}',`problema`='{problema}',`descricao`='{descricao}' WHERE idaviso = '{idaviso}'"
    cursor.execute(sql)
    cursor.close()
    conex.mydb.close()
    return RedirectResponse(url=f"aviso", status_code=303)


@app.get("/listaviso", response_class=HTMLResponse)
async def listaviso(request: Request):
    conex.mydb.reconnect()
    cursor = conex.mydb.cursor()
    sql = "SELECT * FROM aviso"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    cursor.close()
    conex.mydb.close()
    return templates.TemplateResponse("listaviso.html", {"request": request, "aviso": myresult})


if __name__ == '__mail__':
    app.rum()
