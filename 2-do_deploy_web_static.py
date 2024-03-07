#!/usr/bin/python3
'''script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy'''
from fabric.api import run, put, env
from os.path import exists


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']


def do_deploy(archive_path):
    '''Distributes an archive to my web servers'''
    if not exists(archive_path):
        return False

    try:
        archive = archive_path.split('/')[-1].split('.')[0]
        target = '/data/web_static/releases/'+archive
        # upload archive to /tmp/
        put(archive_path, '/tmp/')
        run(f'mkdir -p {target}')
        run(f'tar -xzf /tmp/{archive}.tgz -C {target}')
        run(f'mv /data/web_static/releases/{archive}/web_static/* {target}')
        run(f"rm -rf /data/web_static/releases/{archive}/web_static")
        # remove symbolic link
        run('rm -rf /data/web_static/current')
        # create new link
        run(f'ln -s {target} /data/web_static/current')
        return True
    except Exception:
        return False
