#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of
# 'web_static'

# UPDATE server, but DO NOT UPGRADE: This is because, it takes time to upgrade
# which ALX checker don't have time for
sudo apt-get update

# Install nginx if not already installed
if (("$(pgrep -c nginx)" == 0))
then
    sudo apt-get install nginx -y;
fi

# Create the folder /data/ if it doesn't already exist
if [ ! -d "/data/" ]
then
    mkdir "/data";
fi

# Create the folder /data/web_static/ if it doesn't already exist
if [ ! -d "/data/web_static/" ]
then
    mkdir "/data/web_static";
fi

# Create the folder /data/web_static/releases/ if it doesn't already exist
if [ ! -d "/data/web_static/releases/" ]
then
    mkdir "/data/web_static/releases";
fi

# Create the folder /data/web_static/shared/ if it doesn't already exist
if [ ! -d "/data/web_static/shared/" ]
then
    mkdir "/data/web_static/shared";
fi

# Create the folder /data/web_static/releases/test/ if it doesn't already exist
if [ ! -d "/data/web_static/releases/test/" ]
then
    mkdir "/data/web_static/releases/test";
fi

# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)
echo "Welcome to Rashisky Domain" > /data/web_static/releases/test/index.html;

# Create a symbolic link /data/web_static/current linked to the
# /data/web_static/releases/test/ folder. if already exist, it should be
# deleted and recreated every time the script is ran
if [ -e "/data/web_static/current" ]
then
    sudo rm /data/web_static/current;
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current;

# Give ownership of the /data/ folder to the ubuntu user AND group (you
# can assume this user and group exist). This should be recursive; everything
# inside should be created/owned by the user/group
sudo chown -R ubuntu:ubuntu /data/;

# Update the Nginx configuration to serve the content of /data/web_static/current/
# to hbnb_static (ex: https://mydomainname.tech/hbnb_static)

nginx_config="server {
        listen 80 default_server;
        listen [::]:80;

        root /var/www/html;
        index index.html;

        server_name _;

        location / {
            try_files \$uri \$uri/ =404;
        }

        location /hbnb_static/ {
            alias /data/web_static/current/;
        }
}"

echo "$nginx_config" > /etc/nginx/sites-available/default;

if [ -e "/etc/nginx/sites-enabled/default" ]
then
    sudo rm /etc/nginx/sites-enabled/default;
fi
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default;

# restart nginx
sudo service nginx restart;
