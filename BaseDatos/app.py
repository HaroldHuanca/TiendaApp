from fastapi import FastAPI, Form
from app.database import DatabaseManager
from fastapi.responses import HTMLResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    with DatabaseManager() as db:
        result = db.execute("SELECT * FROM tbl_clientes WHERE documento = %s AND estado = %s", (username, password))
        user = result.fetchone()
        if user:
            return {"mensaje": "Inicio de sesión exitoso"}
        return {"mensaje": "Usuario o contraseña incorrectos"}