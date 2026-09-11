docker build ./backend 

docker run --rm -v ${PWD}/backend:/app -w /app python:3.11-slim bash -c "apt-get update && apt-get install -y git && pip download -r requirements.txt -d wheels"

docker compose up --build 