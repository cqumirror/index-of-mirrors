from fabric.api import env, cd, run, put
from fabric.contrib.files import exists

code_dir = "~/source-git/index-of-mirrors"
target_dir = "/srv/actor"


def pull():
    with cd(code_dir):
        run("git pull")


def prepare():
    actor_env_dir = "env"
    # Create target dir and log dir for actor
    run("mkdir -p /srv/actor/log")
    with cd(target_dir):
        # Create virtual env for actor if not exists and upgrade pip
        if not exists(actor_env_dir):
            run("virtualenv env")
            # Upgrade pip
            run("env/bin/pip install --upgrade pip")
    # Create log dir for gunicorn in /var/log
    run("mkdir -p /var/log/gunicorn")


def put_config_files():
    # Update gunicorn's config
    put("server/gunicorn.py", target_dir)
    put("server/settings.cfg", target_dir)


def deploy():
    put_config_files()
    with cd(code_dir):
        run("rm -rf /srv/actor/actor.bak")
        run("mv /srv/actor/actor{,.bak}")   # Back up
        run("cp -r actor /srv/actor")
        # Update requirements for actor
        run("cp requirements.txt /srv/actor")
        run("cp schema.sql /srv/actor")
        # Update static files
        run("rm -rf /www/mirrors/static.bak")
        run("mv /www/mirrors/static{,.bak}")     # Back up
        run("cp -r actor/static /www/mirrors")


def update_db():
    put("schema.sql", target_dir)
    with cd(target_dir):
        run("mysql -u root -p < schema.sql")


def start():
    with cd(target_dir):
        actor_pid_file = "gunicorn-actor.pid"
        # Reload if actor running
        if exists(actor_pid_file):
            run("export ACTOR_SETTINGS=/srv/actor/settings.cfg && "
                "kill -HUP $(<{})".format(actor_pid_file))
        else:
            # Start new gunicorn processes
            run("export ACTOR_SETTINGS=/srv/actor/settings.cfg && "
                "env/bin/gunicorn -c gunicorn.py actor:app -D")
