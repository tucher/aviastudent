>install.log
exec >  install.log
exec 2> >(tee -a install.log >&2)

errcho() { echo "$@" 1>&2; }

echo -e 'LANG="en_US.UTF-8"\nLC_ALL="en_US.UTF-8"' > /etc/default/locale 
errcho -e "\n\n\n\n\n==================================UPDATING PACKAGES=================================="
apt-get update
apt-get upgrade -y
locale-gen UTF-8


errcho -e "\n\n\n\n\n==================================INSTALLING REQUIRED APT PACKAGES=================================="
apt-get install nginx python3-dev python3-pip  postgresql-server-dev-all postgresql supervisor


errcho -e "\n\n\n\n\n==================================INSTALLING REQUIRED PIP PACKAGES=================================="
echo 'PYTHONIOENCODING="utf-8"' >> /etc/environment 
pip3 install virtualenv 


errcho -e "\n\n\n\n\n==================================CONFIGURING POSTGRESQL=================================="
su - postgres -c "psql -c \"ALTER user postgres with password 'aviastudent';\""
su - postgres -c "createdb aviastudent"


errcho -e "\n\n\n\n\n==================================SETTING UP POSTGRESQL INFRASTRUCTURE=================================="
cp setup_db_sql_query.sql /var/lib/postgresql/
su - postgres -c "psql -d aviastudent -a -f /var/lib/postgresql/setup_db_sql_query.sql"


errcho -e "\n\n\n\n\n==================================SETTING UP aviastudent SERVER=================================="
cp -r www/aviastudent /var/www/
chown -R www-data:www-data /var/www/aviastudent
chmod 755 /var/www
cp nginx/aviastudent /etc/nginx/sites-available/aviastudent
ln -s /etc/nginx/sites-available/aviastudent /etc/nginx/sites-enabled/aviastudent
rm /etc/nginx/sites-enabled/default
service nginx restart
cd ~
virtualenv api-ws-venv
api-ws-venv/bin/pip3 install tornado django psycopg2

mkdir logs
cp aviastudent/network-components/api-ws-server_supervisor.conf /etc/supervisor/conf.d/

service supervisor restart
