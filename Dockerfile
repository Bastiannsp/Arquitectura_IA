# --- Etapa 1: Build (Construcción) ---
# Se usa una imagen de Python completa para instalar dependencias
FROM python:3.10-slim as builder

# Se establece el directorio de trabajo
WORKDIR /app

# Se copian e instalan las dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# --- Etapa 2: Final (Ejecución) ---
# Se usa una imagen 'slim' que es más ligera
FROM python:3.10-slim

WORKDIR /app

# Se copian solo las dependencias pre-compiladas (wheels) de la etapa anterior
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Se copia el código de la aplicación
COPY app.py .

# Se expone el puerto que usará Gunicorn
EXPOSE 5000

# Se crea un usuario no-root para ejecutar la aplicación (Mejor práctica de seguridad)
RUN useradd --system --uid 1001 appuser
USER appuser

# Comando para ejecutar la aplicación en producción usando Gunicorn
# -w 4: Inicia 4 procesos "workers"
# -b 0.0.0.0:5000: Escucha en todas las interfaces en el puerto 5000
# app:app: Hace referencia al objeto 'app' dentro del archivo 'app.py'
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]