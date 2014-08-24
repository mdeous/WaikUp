# -*- coding: utf-8 -*-

from fabric.api import *

DEB_REQUIREMENTS = [
    'apache2',
    'libapache2-mod-wsgi',
    'postgresql',
    'libpq-dev',
    'python',
    'python-dev',
    'openssl',
    'python-virtualenv'
]
SERVICES = [
    'postgresql',
    'apache2'
]
VIRTUALENV_ACTIVATE = '/var/www/waikup/bin/activate'


def venv_run(activate, cmd, folder=None):
    virtualenv = 'source %s' % activate
    with prefix(virtualenv):
        with cd(folder or '.'):
            run(cmd)


@task
def prepare_system():
    sudo('aptitude update', quiet=True)
    sudo('aptitude install -y %s' % ' '.join(DEB_REQUIREMENTS), quiet=True)
    sudo('sysctl -w net.ipv6.conf.all.disable_ipv6=1')


@task
def setup_database():
    run('cp /var/www/waikup/src/setup_testdb.sql /tmp/waikup_setupdb.sql')
    run('cp /var/www/waikup/src/testdb.sql /tmp/waikup_testdb.sql')
    sudo('psql --file=/tmp/waikup_setupdb.sql', user='postgres', quiet=True)
    sudo('psql -d waikup --file=/tmp/waikup_testdb.sql', user='postgres', quiet=True)
    sudo('cp /var/www/waikup/src/pg_hba.conf /etc/postgresql/9.3/main/')
    sudo('echo "listen_addresses = \'*\'" >> /etc/postgresql/9.3/main/postgresql.conf')
    sudo('echo "host waikup waikup 10.0.2.0/24 password" >> /etc/postgresql/9.3/main/pg_hba.conf')
    sudo('service postgresql restart')


@task
def setup_apache():
    sudo('openssl req -x509 -nodes -days 365 -newkey rsa:2048 '
         '-keyout /etc/apache2/server.key -out /etc/apache2/server.crt '
         '-subj /C=US/ST=City/L=City/O=company/OU=SSLServers/CN=localhost/emailAddress=SSLServer@company.com',
         quiet=True
    )
    sudo('cp /var/www/waikup/src/waikup_apache.conf /etc/apache2/sites-available/default.conf')
    sudo('touch /var/www/waikup/.htaccess')
    sudo('a2enmod ssl')
    sudo('a2enmod wsgi')
    sudo('a2dissite 000-default')
    sudo('a2ensite default')
    sudo('service apache2 restart')


@task
def setup_waikup():
    sudo('chmod -R o+w /var/www/waikup')
    run('virtualenv /var/www/waikup')
    venv_run(VIRTUALENV_ACTIVATE, 'python /var/www/waikup/src/setup.py develop', folder='/var/www/waikup/src')
    venv_run(VIRTUALENV_ACTIVATE, 'pip install flask-debugtoolbar')


@task(default=True)
def setup_all():
    execute(prepare_system)
    execute(setup_database)
    execute(setup_apache)
    execute(setup_waikup)
