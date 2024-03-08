# puppet manifest
file {'/data/web_static/releases': ensure => direcory}
file {'/data/web_static/shared': ensure => direcory}
file {'/data/web_static/releases/test/': ensure => direcory}
file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}
file {'/data/web_static/current': ensure => absent}
