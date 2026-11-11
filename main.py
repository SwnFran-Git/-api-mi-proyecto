from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Tareas")
class Tarea(BaseModel):
 titulo: str
 hecha: bool = False
tareas = {}
siguiente_id = 1
@app.get("/")
def inicio():
 return {"mensaje": "Hola, API en la nube"}
@app.get("/saludo/{nombre}")
def saludo(nombre: str, idioma: str = "es"):
 texto = "Hello" if idioma == "en" else "Hola"
 return {"saludo": f"{texto}, {nombre}"}
@app.post("/tareas", status_code=201)
def crear(tarea: Tarea):
 global siguiente_id
 tareas[siguiente_id] = tarea.model_dump()
 siguiente_id += 1
 return {"id": siguiente_id - 1, **tarea.model_dump()}
@app.get("/tareas")
def listar():
 return tareas
@app.get("/tareas/{id}")
def obtener(id: int):
 if id not in tareas:
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tareas[id]
@app.put("/tareas/{id}")
def actualizar(id: int, tarea: Tarea):
 if id not in tareas:
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
 tareas[id] = tarea.model_dump()
 return tareas[id]
@app.delete("/tareas/{id}", status_code=204)
def eliminar(id: int):
 if id not in tareas:
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
 del tareas[id]