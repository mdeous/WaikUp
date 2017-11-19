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


@task
def prepare_system():
    sudo('apt-get update', quiet=True)
    sudo('apt-get install -y %s' % ' '.join(DEB_REQUIREMENTS), quiet=True)
    sudo('pip install pipenv')
    sudo('sysctl -w net.ipv6.conf.all.disable_ipv6=1')


@task
def setup_database():
    sudo('cp /var/www/waikup/src/deploy/pg_hba.conf /etc/postgresql/9.3/main/')
    sudo('echo "listen_addresses = \'*\'" >> /etc/postgresql/9.3/main/postgresql.conf')
    sudo('echo "host waikup waikup 10.0.2.0/24 password" >> /etc/postgresql/9.3/main/pg_hba.conf')
    sudo('service postgresql restart')


@task
def setup_apache():
    sudo('openssl req -x509 -nodes -days 365 -newkey rsa:2048 '
         '-keyout /etc/apache2/server.key -out /etc/apache2/server.crt '
         '-subj /C=US/ST=City/L=City/O=company/OU=SSLServers/CN=localhost/emailAddress=SSLServer@company.com',
         quiet=True)
    sudo('cp /var/www/waikup/src/deploy/waikup_apache.conf /etc/apache2/sites-available/default.conf')
    sudo('touch /var/www/waikup/.htaccess')
    sudo('a2enmod ssl')
    sudo('a2enmod wsgi')
    sudo('a2dissite 000-default')
    sudo('a2ensite default')
    sudo('service apache2 restart')


@task
def setup_waikup():
    sudo('chmod -R o+w /var/www/waikup')
    with cd('/var/www/waikup/src'):
        run('pipenv install')


@task
def restart_services():
    for service in SERVICES:
        sudo('service %s restart' % service)


@task
def init_dev():
    run('cp /var/www/waikup/src/deploy/setup_testdb.sql /tmp/waikup_setupdb.sql')
    run('cp /var/www/waikup/src/deploy/testdb.sql /tmp/waikup_testdb.sql')
    sudo('psql --file=/tmp/waikup_setupdb.sql', user='postgres', quiet=True)
    sudo('psql -d waikup --file=/tmp/waikup_testdb.sql', user='postgres', quiet=True)
    with cd('/var/www/waikup/src'):
        run('pipenv install -d')


@task
def init_prod():
    with cd('/var/www/waikup/src'):
        run('pipenv install')
        run('pipenv run ./manage.py setupdb')


@task(default=True)
def setup_all():
    execute(prepare_system)
    execute(setup_database)
    execute(setup_apache)
    execute(setup_waikup)
    execute(restart_services)
