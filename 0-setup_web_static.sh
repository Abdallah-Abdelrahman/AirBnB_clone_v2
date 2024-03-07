#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

LINK_NAME="/data/web_static/current"

# installed nginx if it's not installed already
[[ ! $(dpkg-query -W nginx) ]] > /dev/null 2>&1 && apt update && apt install nginx -y

mkdir -p /data/web_static/{releases,shared}
mkdir -p /data/web_static/releases/test/
cat << EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# if link exists; remove it, and create it everytime script runs
[ -L "$LINK_NAME" ] && rm "$LINK_NAME"

ln -s /data/web_static/releases/test/ "$LINK_NAME"

# assign ownership
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
# (ex: https://mydomainname.tech/hbnb_static
cat << EOF > /etc/nginx/sites-enabled/default
server {
	add_header X-Served-By $(hostname);

	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files \$uri \$uri/ =404;
	}
	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
	}
	error_page 404 /404.html;
        location = /404.html {
		root /var/www/html;
                internal;
        }
	location /hbnb_static {
		alias /data/web_static/current/;
	}
}
EOF

service nginx restart
