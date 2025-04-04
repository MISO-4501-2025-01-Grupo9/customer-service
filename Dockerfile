# Usa una imagen base ligera de Python 3.12
FROM python:3.12-slim

WORKDIR /app

# Copia requirements.txt e instala las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto parametrizado (por defecto 8087)
EXPOSE ${PORT}

# Variables de entorno por defecto
ENV DATABASE_URL=postgresql://myuser:mypass@db:5432/mydatabase
ENV PORT=8080
ENV HOST=0.0.0.0
ENV FLASK_ENV=production
ENV SAFRS_API_DOCS_URL=/api/swagger.html

CMD ["python", "app.py"]
