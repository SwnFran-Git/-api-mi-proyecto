from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from os import getenv

# --- main.py (Lectura de Variables de Entorno) ---
from dotenv import load_dotenv










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
 # --- main.py (Endpoint Health Check) ---

@app.get("/health", tags=["Sistema"])
def health_check():
    return {
        "status": "online",
        "ambiente": getenv("ENVIRONMENT", "desarrollo_local"),
        "servidor": "FastAPI + Uvicorn Cloud"
    }
   
if __name__ == "__main__":
    import uvicorn
    # Lee el puerto inyectado por el PaaS; si no existe, usa 8000 por defecto
    puerto = int(getenv("PORT", 8000))
    # Escucha obligatoria en 0.0.0.0 para entornos en la nube
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)


@app.get("/version", tags=["Sistema"])
def consultar_version():
    return {
        "version": "1.2.0",
        "descripcion": "API desplegada mediante Continuous Deployment desde GitHub",
        "docente": "Lic. Ronald J. Villar Gonzales",
        "institucion": "IES República Federal de Alemania - Chiclayo"
    }



# Carga las variables del archivo .env local si existe
load_dotenv()

SECRET_KEY = getenv("API_SECRET_KEY", "clave_por_defecto_insegura")
MODO_DEBUG = getenv("MODO_DEBUG", "False")

@app.get("/config-check", tags=["Seguridad"])

def config_check():
    return {
        "modo_debug": MODO_DEBUG,
        # Buena práctica: nunca reveles el valor completo del secreto en logs o endpoints
        "clave_configurada": True if SECRET_KEY != "clave_por_defecto_insegura" else False,
        "prefijo_clave": SECRET_KEY[:4] + "****"
    }

