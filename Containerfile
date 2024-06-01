FROM --platform=linux/amd64 python:3.12 as backend
WORKDIR /src
ENV PYTHONUNBUFFERED 1
ADD requirements.txt .
RUN --mount=type=cache,target=/root/.cache python -m venv venv && venv/bin/pip install -U pip && venv/bin/pip install -r requirements.txt
ADD . /src
COPY conf/_env .env
RUN venv/bin/python manage.py collectstatic --noinput && rm .env
RUN venv/bin/python -m blacknoise.compress static
RUN useradd -U -d /src deploy
USER deploy
EXPOSE 8000
CMD ["venv/bin/python", "-m", "granian", "--interface", "asgi", "asgi:application", "--workers", "2", "--host", "0.0.0.0", "--port", "8000", "--respawn-failed-workers"]
