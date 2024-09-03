FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY . .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Establece la variable de entorno para Flask
ENV FLASK_APP=src/app.py

# Define el comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
