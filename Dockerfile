# Gunakan image dasar Python
FROM python:3.9-slim

# Salin aplikasi ke container
WORKDIR /app
COPY app/ /app/

# Salin requirements.txt dan instal dependensi
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "main.py"]
