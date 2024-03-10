#!/usr/bin/python3
'''script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy

Attrs:
    env: enviroment variables for fabric
'''
from fabric.api import put, env, sudo
from os.path import exists


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    '''Distributes an archive to my web servers'''
    if not exists(archive_path):
        return False

    try:
        # extract archive name w/out extension
        archive = archive_path.split('/')[-1].split('.')[0]
        target = f'/data/web_static/releases/{archive}'
        # upload archive to /tmp/
        put(archive_path, '/tmp/')
        sudo(f'mkdir -p {target}')
        sudo(f'tar -xzf /tmp/{archive}.tgz -C {target}')
        sudo(f'rm /tmp/{archive}.tgz')
        sudo(f'rsync -a {target}/web_static/ {target}')
        sudo(f'rm -rf {target}/web_static')
        # remove symbolic link
        sudo('rm -rf /data/web_static/current')
        # create new link
        sudo(f'ln -s {target} /data/web_static/current')
        print("New version deployed!")

        return True
    except Exception:
        return False
