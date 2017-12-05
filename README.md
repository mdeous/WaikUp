[![Maintainability](https://api.codeclimate.com/v1/badges/2ddc51217828000b8267/maintainability)](https://codeclimate.com/github/mattoufoutu/WaikUp/maintainability)

# WaikUp
Collaborative news sharing platform.

## Introduction
WaikUp is an application to share links found around the Web with a group of people.
It is written in Python using the Flask framework.

Additionally to the web interface, WaikUp provides a RESTful API to allow
interacting with the application programatically.

## Screenshots
Links list:
![links_list](docs/links_list.png)

Expanded link description:
![links_list_expanded](docs/links_list_expanded.png)

Link submition:
![submit_link](docs/submit_link.png)

User profile:
![user_profile](docs/user_profile.png)

## Dependencies
* Python2
* A bunch of Python modules (see [`Pipfile`](Pipfile) for details)

## Management Utility
The documentation for management commands is available [here](docs/MANAGEMENT.md)

## API
The API documentation is available [here](docs/API.md).

A Javascript library for the API is available in `waikup/static/js/WaikupAPI.js`, and can
be used either included from the server (`https://waikup-host/static/js/WaikupAPI.js`).

## Deployment

### Docker
The project provides a `Dockerfile` as well as a `docker-compose` configuration for easier
deployment. A `Makefile` is also provided to abstract image creation and container execution.

The following `make` targets are available:
* `build` (default) - builds a `mdeous/waikup:latest` image
* `run` - runs `docker-compose` with a waikup+nginx+postgresql+postfix stack

### Manual Deployment
A dedicated documentation page is available [here](docs/DEPLOY.md).

### Development Environment
To create a development environment, the only mandatory dependency is a properly configured
Postgresql server with the correct database and user created. The SMTP server is only required
to test email distribution.

Once the Postgresql server is up and running (see deployment documentation for details),
the development environment can be created using the following commands:

```bash
pipenv install -d  # create the virtulenv and install dependencies
pipenv shell  # activate the virtualenv
python manage.py setupdb  # create database structure
python manage.py adduser --admin  # create a new administrator
python manage.py runserver -r -d  # start Flask development server
```

### Sending Emails
Emails can be sent using the `./manage.py sendmail` command, if you want to automate this, 
just set a `crontab` entry to run this command periodically (make sure to run it using the 
virtualenv's Python interpreter, this can be done with pipenv: `pipenv run ./manage.py sendmail`) 
When running this command, all active emails will be archived.

### Settings
:warning: **`SECRET_KEY` and `SECURITY_PASSWORD_SALT` should be replaced with random values 
for production use** :warning:

Default settings value are stored in the `waikup/settings.py` file. These values can be
overriden by creating a `prod_settings.py` file in the same directory and storing custom
configuration values in this file.

The `settings.py` file doesn't contain every available setting though, for a complete list,
please refer to Flask and used plugins documentation (see [`Pipfile`](Pipfile) for 
a complete plugins list).

A table describing every setting available in the `settings.py` file, its default value, 
and the environment variable from which they can alternatively be set, is available
[here](docs/SETTINGS.md "Settings list").

## Issues and Contributions
If you encounter any bug, or think a particular feature is missing, feel free to open a
ticket, or even better, fork the repository and make a pull request with your changes! ;)

Contribution guidelines are available [here](docs/CONTRIBUTING.md).

## Licensing
This project is licensed under the GNU General Public License v3.
