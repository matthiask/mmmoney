FROM --platform=linux/amd64 python:3.12 as backend
WORKDIR /src
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/usr/local
ADD requirements.txt .
RUN pip install uv && uv pip install -r requirements.txt --system
ADD . /src
COPY conf/_env .env
RUN python manage.py collectstatic --noinput && rm .env
RUN python -m blacknoise.compress static
RUN useradd -U -d /src deploy
USER deploy
EXPOSE 8000
CMD ["python", "-m", "granian", "--interface", "asgi", "asgi:application", "--workers", "2", "--host", "0.0.0.0", "--port", "8000", "--respawn-failed-workers"]
