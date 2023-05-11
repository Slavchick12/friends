FROM python:3.10.7-buster
WORKDIR /app
COPY requirements.txt .
RUN apt update && \
    apt upgrade -y && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn==20.0.4
COPY . .
CMD ["gunicorn", "friends.wsgi", "-b", "0.0.0.0:8000"]