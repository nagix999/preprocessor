# syntax=docker/dockerfile:1.7-labs

FROM python:3.10-slim

RUN mkdir -m 777 -p /root/.cache/datalab

COPY datalab /root/.cache/datalab

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

COPY --exclude=datalab/ . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]