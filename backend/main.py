from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import shutil
from core import process_audio

app = FastAPI(title="PrismAudio API")

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Servir archivos estáticos (para acceder a los audios procesados)
# Esto permitirá acceder a http://localhost:8069/files/nombre_cancion/vocals.wav
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
def read_root():
    return {"status": "online", "app": "PrismAudio Backend"}

@app.post("/separate/")
async def separate_audio_endpoint(file: UploadFile = File(...)):
    # 1. Guardar el archivo subido
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Procesar con Spleeter
    # Nota: spleeter creará una carpeta dentro de uploads con el nombre del archivo
    result = process_audio(file_location, UPLOAD_DIR)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
        
    # 3. Retornar las URLs para acceder a los archivos
    # Construimos las URLs relativas a nuestro mount "/files"
    return {
        "message": "Separation complete",
        "original": file.filename,
        "vocals_url": f"/files/{result['vocals']}",
        "accompaniment_url": f"/files/{result['accompaniment']}"
    }

# --- SERVIR FRONTEND EN PRODUCCIÓN ---
# Si existe la carpeta dist del frontend, servimos el index.html
FRONTEND_DIST = os.path.join(os.path.dirname(BASE_DIR), "frontend", "dist")

if os.path.exists(FRONTEND_DIST):
    # Montar archivos estáticos del build (JS, CSS, assets)
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Si la ruta es un archivo (tiene extensión), intentamos servirlo
        if "." in full_path:
             file_path = os.path.join(FRONTEND_DIST, full_path)
             if os.path.exists(file_path):
                 return FileResponse(file_path)
        
        # Para cualquier otra ruta (o la raíz), devolvemos index.html (SPA routing)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8069)
