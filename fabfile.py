from fabric.api import *


env.forward_agent = True
env.hosts = ['mmmoney.406.ch']


@task
def deploy():
    local('git push origin master')
    with cd('/var/www/mk/mmmoney'):
        run('git checkout master') # yes.
        run('git pull')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements.txt')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py syncdb')
        #with cd('tomac/static/tomac'):
            #run('GEM_HOME=/home/mk/_gems/ /home/mk/_gems/bin/compass compile -s compressed')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sudo supervisorctl restart mk_mmmoney')
