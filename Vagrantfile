# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$setup_script = <<SCRIPT
aptitude update
aptitude install -y apache2 libapache2-mod-wsgi postgresql libpq-dev python-virtualenv python-dev
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/server.key -out /etc/apache2/server.crt -subj /C=US/ST=City/L=City/O=company/OU=SSLServers/CN=localhost/emailAddress=SSLServer@company.com
cp /var/www/waikup/src/waikup_apache.conf /etc/apache2/sites-available/default
cp /var/www/waikup/src/setup_testdb.sql /tmp/waikup_setupdb.sql
chmod 777 /tmp/waikup_setupdb.sql
cp /var/www/waikup/src/testdb.sql /tmp/waikup_testdb.sql
chmod 777 /tmp/waikup_testdb.sql
su postgres -c "psql --file=/tmp/waikup_setupdb.sql"
su postgres -c "psql -d waikup --file=/tmp/waikup_testdb.sql"
cp /var/www/waikup/src/pg_hba.conf /etc/postgresql/9.1/main/
echo "listen_addresses = '*'" >> /etc/postgresql/9.1/main/postgresql.conf
echo "host waikup waikup 10.0.2.0/24 password" >> /etc/postgresql/9.1/main/pg_hba.conf
service postgresql restart
touch /var/www/waikup/src/.htaccess
a2enmod ssl
service apache2 restart
chmod -R o+w /var/www/waikup
su vagrant -c "virtualenv /var/www/waikup && \
source /var/www/waikup/bin/activate && \
cd /var/www/waikup/src && \
python setup.py develop && \
pip install flask-debugtoolbar"
SCRIPT
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  config.vm.network :forwarded_port, guest: 443, host: 8443
  config.vm.network :forwarded_port, guest: 5432, host: 65432
  config.vm.synced_folder ".", "/var/www/waikup/src",
    id: "src",
    owner: "vagrant",
    group: "www-data",
    mount_options: ["dmode=775,fmode=664"]

  config.vm.provider :virtualbox do |vb|
    vb.gui = false
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.provision :shell do |sh|
    sh.inline = $setup_script
  end

end
