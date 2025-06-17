FROM python:3.10-slim

WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and model
COPY app/ ./app/
COPY app/mango_classifier_model.h5 ./app/

# Command to run
CMD ["python", "app/main.py"]
