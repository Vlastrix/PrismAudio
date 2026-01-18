@echo off
echo Iniciando PrismAudio...
echo Por favor espere mientras se carga el servidor...

:: Iniciar el backend en segundo plano (asumiendo que python está en el PATH)
start "PrismAudio Backend" python backend/main.py

:: Esperar unos segundos para dar tiempo al servidor de arrancar
timeout /t 5 /nobreak >nul

:: Abrir el navegador
start http://localhost:8069

echo Servidor iniciado. No cierre la ventana negra de fondo.
pause
