FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["python", "-m", "server.app_server"]