FROM python:3.12 as backend
WORKDIR /src
ENV PYTHONUNBUFFERED 1
ADD . /src
RUN --mount=type=cache,target=/root/.cache python -m venv venv && venv/bin/pip install -U pip && venv/bin/pip install -r requirements.txt
COPY conf/_env .env
RUN venv/bin/python manage.py collectstatic --noinput && rm .env
RUN useradd -U -d /src deploy
USER deploy
EXPOSE 8000
CMD ["venv/bin/granian", "--interface", "wsgi", "wsgi:application", "--workers", "2", "--host", "0.0.0.0", "--port", "8000", "--access-log"]
