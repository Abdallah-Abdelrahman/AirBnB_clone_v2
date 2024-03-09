# puppet manifest to configure nginx
$dirs = ['/data/', '/data/web_static/', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test/']

package {'nginx': ensure => installed}

file {$dirs: ensure => 'directory'}
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
      <head>
      </head>
      <body>
        Holberton School
      </body>
    </html>'
    ,
  require => File['/data/web_static/releases/test/']
}
file {'/data/web_static/current': ensure => 'link', target => '/data/web_static/releases/test/'}

# change ownership recursively
exec {'chown -R ubuntu:ubuntu /data/': path => '/usr/bin/:/usr/local/bin/:/bin/',}

file {'/etc/nginx/sites-enabled/default':
  ensure  => present,
  content => "server {
	add_header X-Served-By ${hostname};

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
  }",
  require => Package['nginx'],
}

service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => File['/etc/nginx/sites-enabled/default'],  # Ensure the Nginx configuration file is present before restarting the service
  subscribe => File['/etc/nginx/sites-enabled/default'], # Restart the service whenever the configuration file changes
}
