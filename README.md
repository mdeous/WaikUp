# WaikUp

Collaborative news sharing platform.

## Introduction

WaikUp is an application for teams who want a collaborative platform to share their
findings around the Web.

## WebUI + RESTful API

Additionally to the traditionnal web interface, WaikUp provides a RESTful API to allow
any other interface (browser extension, mobile application, etc...) to be built upon.

## Version control workflow

Development of this application and its features use the `git-flow` workflow, to ensure
feature's code are separated from the stable (`master`) branch, and stable code remains,
well... stable!

The complete workflow is explained in details on
[this page](http://nvie.com/posts/a-successful-git-branching-model/ "A successful branching model"),
and the `git-flow` utility can be found [here](https://github.com/nvie/gitflow "Git-Flow").

## API endpoints & parameters

### Links API

* `/api/links/` [GET] - Get all links in database
* `/api/links/<id>` [GET] - Get link with given ID
* `/api/links/` [POST+Auth] - Create a new link
    * `url` (required)
    * `title` (required)
    * `description`
* `/api/links/<id>` [PUT+Owner] - Update informations for link with given ID
    * `url`
    * `title`
    * `description`
* `/api/links/<id>` [DELETE+Owner] - Delete link with given ID

### Users API

* `/api/users/` [GET+Admin] - Get all users in database
* `/api/users/<id>` [GET+Admin] - Get user with given ID
* `/api/users/` [POST+Admin] - Create a new user
    * `username` (required)
    * `first_name` (required)
    * `last_name` (required)
    * `email` (required)
    * `password` (required)
* `/api/links/<id>` [PUT+Admin] - Update informations for user with given ID
    * `first_name`
    * `last_name`
    * `email`
    * `password`
* `/api/links/<id>` [DELETE+Admin] - Delete user with given ID

## Deployment

Deploying the application for production use requires to use a standalone Web server. This documentation
describes the procedure using the Apache web server on a debian based system.

* Make sure that the following packages are installed on the system:
    * `apache2`
    * `libapache2-mod-wsgi`
    * `postgresql`
    * `libpq-dev`

* Enable SSL using `a2enmod ssl` and generate the appropriate certificates in `/etc/apache2`.
* Create a new virtualenv in `/var/www`, and clone the repository into the virtualenv's `src` folder:


    cd /var/www
    virtualenv waikup
    chmod +x waikup
    cd waikup
    git clone git@bitbucket.org:MatToufoutu/waikup.git src


* Activate the newly created virtualenv and install the application:


    source bin/activate
    cd src
    python setup.py install


* Configure Apache using the settings provided in the `waikup.wsgi` file.
* Create a `/var/www/waikup/src/waikup/prod_settings.py` file with (at least) the following values defined:
  * `DEBUG = False`
  * `SECRET_KEY = 'some secret key'` (can be generated using `''.join(choice(string.printable) for _ in range(32))`)

* Setup the database schema using the `waikup_manage setupdb` management command.

When setting up the database, an admin user is created with 'admin:admin' credentials, this account is only meant for
testing purpose, if you are deploying WaikUp in a production environment, immediately create a new admin user using the
`waikup_manage adduser` command, and delete this one (once logged, this can be done from the admin interface).

An API user is also created which username is 'waikupapi', this account is internal and should not be modified or deleted.
It is created with a very strong random password, and can not be used as a normal user.

For a list of settings you might wish to change (database, emails), have a look at the `waikup/settings.py` file.

Emails can be sent using the `waikup_manage sendmail` command, if you want to automate this, just set a `crontab` entry
to run this command periodically. When running this command, all active emails will be archived.
