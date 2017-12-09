# Deployment

## Requirements
To run WaikUp, the following software and services are needed:
* Python
* Pipenv
* uWSGI
* PostgreSQL server
* Mail server (not strictly required for development, except for testing 
  mailing features)
* Reverse proxy server (preferably nginx, only required for production deployment)

For details about installing and configuring these dependencies, please refer
to their own documentation.

## Installation
Clone source code and install dependencies:
```bash
git clone https://github.com/mattoufoutu/waikup
cd waikup
pipenv install -d
pipenv shell
```

Prepare the database:
```bash
su postgres -c "createuser -DPRS waikup"
# use "waikup" as the password when prompted
su postgres -c "createdb -O waikup waikup"
./manage.py setupdb
```

## Development Mode
Simply run Flask's integrated development server:
```bash
FLASK_APP=waikup/application.py flask run --reload
```

## Production Mode
TODO

## Post-Install
* Create a `waikup/prod_settings.py` file with (at least) the following entries:
```python
SECRET_KEY = 'secret key'
SECURITY_PASSWORD_SALT = 'passwords salt' 
DATABASE_PASSWORD = 'db connection password'
MAIL_USERNAME = 'smtp user'
MAIL_PASSWORD = 'smtp password'
MAIL_DEFAULT_SENDER = 'waikup@mydomain'
```

The `SECRET_KEY` and `SECURITY_PASSWORD_SALT` variables are used respectively to 
encrypt/sign session data, and to complexify password hashes, both should be set 
to some long random string.

Safe values for can be generated using the following code (eg. from a Python shell):
```python
import os
from binascii import hexlify
print(hexlify(os.urandom(64)))
```

For a list of other settings you might wish to change (database, emails), have a 
look at the [SETTINGS.md](SETTINGS.md) file.
 
Now, create a new admin user using the `./manage.py adduser -a` command (you can 
create more users later from the Web interface).

The WaikUp instance is now ready for use.
