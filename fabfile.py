from fabric.api import *


HOST = 'deploy@mmmoney.406.ch'


env.forward_agent = True
env.hosts = [HOST]


@task(alias='ws')
def watch_styles():
    local('compass watch mmmoney/static/mmmoney')


@task
def deploy_styles():
    local('compass clean mmmoney/static/mmmoney')
    local('compass compile -s compressed mmmoney/static/mmmoney')
    local('scp -r mmmoney/static/mmmoney/stylesheets %s:www/mmmoney/static/mmmoney/' % HOST)


@task
def deploy():
    deploy_styles()

    local('git push origin master')
    with cd('www/mk/mmmoney'):
        run('git fetch')
        run('git reset --hard origin/master')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements/live.txt')
        run('venv/bin/python manage.py syncdb')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sudo service www-mk_mmmoney restart')


@task
def pyflakes():
    # pip install pyflakes
    local('pyflakes mmmoney/ | grep -v migrations')
