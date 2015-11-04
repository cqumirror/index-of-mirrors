from fabric.api import cd, run, put
from fabric.contrib.files import exists

code_dir = "~/source-git/index-of-mirrors"
target_dir = "/srv/actor"


def pull():
    with cd(code_dir):
        run("git pull")


def prepare():
    actor_env_dir = ".pyenv"
    # create target dir and log dir for actor
    run("mkdir -p /srv/actor/log")
    with cd(target_dir):
        # create virtualenv for actor if not exists and upgrade pip
        if not exists(actor_env_dir):
            run("virtualenv .pyenv")
        # upgrade pip
        run(".pyenv/bin/pip install --upgrade pip")
        # init the pyenv
        run(".pyenv/bin/pip install --upgrade -r requirements.txt --allow-external mysql-connector-python")
    # create log dir for gunicorn in /var/log
    run("mkdir -p /var/log/gunicorn")


def put_config_files():
    # update gunicorn's config
    put("production_confs/gunicorn.py", target_dir)
    put("production_confs/settings.cfg", target_dir)


def deploy():
    put_config_files()
    with cd(code_dir):
        run("rm -rf /srv/actor/actor.bak")
        run("mv /srv/actor/actor{,.bak}")   # back up
        run("cp -r actor /srv/actor")
        # update requirements for actor
        run("cp requirements.txt /srv/actor")
        run("cp schema.sql /srv/actor")
        # update static files
        run("rm -rf /www/mirrors/static.bak")
        run("mv /www/mirrors/static{,.bak}")     # back up
        run("cp -r actor/static /www/mirrors")


def update_db():
    put("schema.sql", target_dir)
    with cd(target_dir):
        run("mysql -u root -p < schema.sql")


def start():
    with cd(target_dir):
        actor_pid_file = "gunicorn-actor.pid"
        # kill old processes gracefully if actor running
        if exists(actor_pid_file):
            run("kill -TERM $(<{})".format(actor_pid_file))
        # start new gunicorn processes
        run("export ACTOR_SETTINGS=/srv/actor/settings.cfg && "
            ".pyenv/bin/gunicorn -c gunicorn.py actor:app -D")

