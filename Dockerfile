FROM python:3.12-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    fonts-liberation libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libdrm2 libgbm1 \
    chromium chromium-driver

# Instala Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código
COPY . /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
