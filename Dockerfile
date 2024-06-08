FROM python:3.10.10

WORKDIR /app

# Copiamos los archivos de requisitos
COPY ./requirements.txt .

# Instalamos requerimientos principales
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./main.py .

EXPOSE 3000
