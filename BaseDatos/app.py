from fastapi import FastAPI, Form
from app.database import DatabaseManager
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    with DatabaseManager() as db:
        result = db.execute("SELECT * FROM tbl_clientes WHERE documento = %s AND estado = %s", (username, password))
        user = result.fetchone()
        if user:
            return {"mensaje": "Inicio de sesión exitoso"}
        return {"mensaje": "Usuario o contraseña incorrectos"}