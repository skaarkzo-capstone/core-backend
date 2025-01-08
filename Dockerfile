FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Use no-cache-dir to disable cache, making Docker image small
RUN pip install --no-cache-dir -r requirements.txt

# Copying application files
COPY . .

EXPOSE 8000
# Only use --reload for uvicorn in local environments as it's for development purposes!!!!
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]