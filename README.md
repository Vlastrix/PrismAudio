# PrismAudio 🎵

PrismAudio es una aplicación web impulsada por Inteligencia Artificial para separar la voz y la parte instrumental de archivos de audio y video.

## 🚀 Instalación y Setup (Usuario Final)

Para que funcione en otra computadora sin complicaciones, hemos simplificado todo para que solo requiera **Python**.

### Prerrequisitos
1.  **Python 3.8+**: [Descargar aquí](https://www.python.org/downloads/).
    *   *Importante*: Al instalar, marca la casilla **"Add Python to PATH"**.
2.  **FFmpeg**: Necesario para el procesamiento de audio.
    *   Descargar y extraer.
    *   Agregar la carpeta `bin` de FFmpeg a las Variables de Entorno (PATH).

### Pasos Rápidos (Windows)
1.  Descarga este código.
2.  Ejecuta el archivo `install_dependencies.bat` (lo crearemos para instalar librerías automáticamente).
3.  Haz doble clic en `start_windows.bat`.
4.  ¡Listo! Se abrirá el navegador con la aplicación.

---

## 🛠️ Setup para Desarrolladores

Si quieres modificar el código, necesitas ejecutar Backend y Frontend por separado.

### 1. Backend (Python/FastAPI)
Terminal 1:
```bash
cd backend
pip install -r requirements.txt
python main.py
```
*Corre en: http://localhost:8069*

### 2. Frontend (React/Vite)
Terminal 2:
```bash
cd frontend
npm install
npm run dev
```
*Corre en: http://localhost:5173*

---

## 📦 Modo "Todo en Uno" (Recomendado para distribuir)

Para no tener que instalar Node.js en la otra PC, hacemos una "Build" del frontend y dejamos que Python lo sirva.

1.  **Construir Frontend**:
    ```bash
    cd frontend
    npm run build
    ```
    *Esto crea la carpeta `frontend/dist` con los archivos optimizados.*

2.  **Ejecutar Backend Integrado**:
    El backend está configurado para buscar la carpeta `dist`. Si existe, la sirve en la raíz `/`.
    ```bash
    python backend/main.py
    ```
    *Ahora accedes a todo (App + API) desde http://localhost:8069*
