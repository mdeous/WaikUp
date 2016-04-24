# Deployment

## Development

For development purpose, it is possible to deploy the application on a Vagrant box using the Vagrantfile provided in
the `deploy` folder. The code served by the box is just the local folder mounted in the VM, so while you develop,
any change made will be immediately visible.

As the VM provisioning is done using a Fabric plugin for Vagrant, you also need to install it:


    vagrant plugin install vagrant-fabric


The application can then be fully deployed using a single command:


    vagrant up



## Production

While Flask's built-in server is perfect during development, deploying the application for production use requires to 
use a standalone Web server. This documentation describes the procedure using the Apache web server on a debian based 
system.


### The lazy way

As the Vagrantfile uses Fabric for provisioning, it is as well possible to use Fabric to deploy to your production
server. Create a `/var/www/waikup` folder on your server, then clone WaikUp's repository to an `src` folder inside
the previously created one. Transfer the `/var/www/waikup/src/deploy/fabfile.py` file to your local machine, and run:


    fab -i <ssh_private_key> -H <host> setup_all
    fab -i <ssh_private_key> -H <host> init_prod


Once the deployment is finished, ssh to your server and create a new admin user using the `waikup_manage` utility:


    source /var/www/waikup/bin/activate
    waikup_manage adduser -a
  

You can now replace the auto-generated Apache's certificates for a signed one, and you're good to go!


### The manual way

* Make sure that the following packages are installed on the system:
    * `apache2`
    * `libapache2-mod-wsgi`
    * `postgresql`
    * `libpq-dev`

* Enable Apache's SSL module using `a2enmod ssl` and generate the appropriate certificates in `/etc/apache2`.
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
* Setup the database schema using the `waikup_manage setupdb` management command.


## Post-install

### Settings

* Create a `/var/www/waikup/src/waikup/prod_settings.py` file with (at least) the following values defined:
  * `DEBUG = False`
  * `SECRET_KEY = 'some complicated secret key'` (can be generated using `''.join(choice(string.printable) for _ in range(32))`)
  * `SECURITY_PASSWORD_SALT = 'some complicated salt to be used when hashing passwords'` 

(safe values for `SECRET_KEY` and `SECURITY_PASSWORD_SALT` can be generated using 
`''.join(choice(string.printable) for _ in range(32))`)

For a list of other settings you might wish to change (database, emails), have a look at the `waikup/settings.py` file.
 
* Create a new admin user using the `waikup_manage adduser -a` command (you can create more users later from the WebUI).


### Sending emails

Emails can be sent using the `waikup_manage sendmail` command, if you want to automate this, just set a `crontab` entry
to run this command periodically (make sure to run it using the virtualenv's Python interpreter, which is located at
`/var/www/waikup/bin/python`.) When running this command, all active emails will be archived.
