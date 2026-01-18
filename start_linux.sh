#!/bin/bash
echo "Iniciando PrismAudio..."

# Activar entorno virtual si existe, o usar python del sistema
# source venv/bin/activate 2>/dev/null

# Iniciar servidor
python3 backend/main.py &

# Esperar un poco
sleep 3

# Abrir navegador (intentar xdg-open)
if which xdg-open > /dev/null
then
  xdg-open http://localhost:8069
fi

echo "PrismAudio corriendo en http://localhost:8069"
wait
