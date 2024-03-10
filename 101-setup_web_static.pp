# puppet manifest to configure nginx
$dirs = ['/data/', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']

package {'nginx': ensure => present, provider => 'apt'}

file {$dirs: ensure => directory, require => Package['nginx']}

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

file {'/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  require => '/data/web_static/releases/test/index.html'
}

# change ownership recursively
exec {'chown -R ubuntu:ubuntu /data/': path => '/usr/bin/:/usr/local/bin/:/bin/', require => File['/data/web_static/current']}

file {'/var/www/html': ensure => present}

file {'/etc/nginx/sites-available/default':
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
  require => File['/var/www/html'],
}
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School\n",
  require => File['/var/www/html'],
}

file { '/var/www/html/custom_404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
  require => File['/var/www/html'],
}

# Restart Nginx
exec { 'nginx restart':
  path    => '/etc/init.d/',
  require => File['/etc/nginx/sites-available/default'],
}
