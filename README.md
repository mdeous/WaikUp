# WaikUp

Collaborative news sharing platform.

## Introduction

WaikUp is an application for teams who want a collaborative platform to share their
findings around the Web.

## API-centric

This application is entirely built around a RESTful API, allowing to build any interface
on top of it, be it a traditionnal WebUI, a browser extension, or a mobile application.

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

* `/api/users/auth` [POST] - Retrieve an authentication token
    * `username` (required)
    * `password` (required)
* `/api/users/deauth` [POST+Auth] - Delete authentication token
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
