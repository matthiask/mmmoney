import os
from fabric.api import cd, env, local, run, task


CONFIG = {
    "host": "www-data@mmmoney.406.ch",
    "domain": "mmmoney.406.ch",
    "project": "mmmoney",
    "branch": "master",
}


env.forward_agent = True
env.hosts = [CONFIG["host"]]


def _configure(fn):
    def _dec(string, *args, **kwargs):
        return fn(string.format(**CONFIG), *args, **kwargs)

    return _dec


local = _configure(local)
cd = _configure(cd)
run = _configure(run)


@task
def install():
    if not os.path.isdir("venv"):
        if os.path.exists("venv"):
            print("venv exists, but is not a folder. Aborting.")
            return

        local("virtualenv venv")

    local("venv/bin/pip install -r requirements.txt")


@task
def dev():
    import socket
    from threading import Thread

    jobs = [Thread(target=runserver)]
    try:
        socket.create_connection(("localhost", 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(Thread(target=lambda: local("redis-server")))
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task(alias="rs")
def runserver(port=8000):
    local("venv/bin/python -Wall manage.py runserver 0.0.0.0:{}".format(port))


@task
def deploy():
    local("flake8 .")
    local("git push origin {branch}")
    with cd("{domain}"):
        run("git fetch")
        run("git reset --hard origin/{branch}")
        run('find . -name "*.pyc" -delete')
        run("venv/bin/pip install -r requirements.txt")
        run("venv/bin/python manage.py migrate")
        run("venv/bin/python manage.py collectstatic --noinput")
        run("systemctl --user restart gunicorn@mmmoney.406.ch.service")


@task
def pull_database():
    local("dropdb --if-exists mmmoney")
    local("createdb mmmoney")
    local('ssh fh06 "source .profile && pg_dump -Ox mk_mmmoney" | psql mmmoney')


@task
def update_requirements():
    local("rm -rf venv requirements.txt")
    local("virtualenv venv")
    local("venv/bin/pip install -U -r requirements-to-freeze.txt")
    local("venv/bin/pip freeze -l | grep -v pkg-resources > requirements.txt")
