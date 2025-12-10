from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pathlib import Path

app = FastAPI()

# Habilitar CORS para poder probar desde el navegador (index.html)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir el archivo index.html desde la raíz para facilitar la prueba
ROOT = Path(__file__).resolve().parent

@app.get("/", include_in_schema=False)
def root_index():
    """Devuelve el index de prueba (archivo estático)."""
    index_file = ROOT / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    raise HTTPException(status_code=404, detail="index.html no encontrado")

# -----------------------
# Datos dentro del programa
# -----------------------
usuarios = [
    {"id": 1, "nombre": "Harold"},
    {"id": 2, "nombre": "Ana"}
]

# Modelo para validar datos
class Usuario(BaseModel):
    nombre: str


# -----------------------
# Métodos HTTP
# -----------------------

# GET: Obtener todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

# GET: Obtener un usuario por ID
@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int):
    for u in usuarios:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# POST: Crear un usuario nuevo
@app.post("/usuarios")
def crear_usuario(user: Usuario):
    nuevo = {
        "id": usuarios[-1]["id"] + 1 if usuarios else 1,
        "nombre": user.nombre
    }
    usuarios.append(nuevo)
    return nuevo

# PUT: Actualizar un usuario existente
@app.put("/usuarios/{user_id}")
def actualizar_usuario(user_id: int, user: Usuario):
    for u in usuarios:
        if u["id"] == user_id:
            u["nombre"] = user.nombre
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# DELETE: Eliminar un usuario
@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    for u in usuarios:
        if u["id"] == user_id:
            usuarios.remove(u)
            return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
