#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

LINK_NAME="/data/web_static/current"
LOCATION="location /hbnb_static {\n\t\talias $LINK_NAME;\n\t}"

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
sed -i "/pass PHP/a\\\t$LOCATION" /etc/nginx/sites-enabled/default

nginx -s reload
