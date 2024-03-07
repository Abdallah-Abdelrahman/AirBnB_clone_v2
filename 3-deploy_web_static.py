#!/usr/bin/python3
'''Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy'''
from fabric.api import local, run, env, put
from datetime import datetime
from os.path import exists


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']


def do_deploy(archive_path):
    '''Distributes an archive to my web servers'''
    if not exists(archive_path):
        return False

    try:
        archive = archive_path.split('/')[-1].split('.')[0]
        target = f'/data/web_static/releases/{archive}/'
        # upload archive to /tmp/
        put(archive_path, '/tmp/')
        run(f'mkdir -p {target}')
        run(f'tar -xzf /tmp/{archive}.tgz -C {target}')
        run(f'rm /tmp/{archive}.tgz')
        run(f'mv /data/web_static/releases/{archive}/web_static/* {target}')
        run(f'rm -rf /data/web_static/releases/{archive}/web_static')
        # remove symbolic link
        run('rm -rf /data/web_static/current')
        # create new link
        run(f'ln -s {target} /data/web_static/current')
        return True
    except Exception:
        return False


def do_pack():
    '''Generate .tgz archive from web_static dir'''
    try:
        local('mkdir -p versions')
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive = 'web_static_' + time + '.tgz'

        # generate archive in current directory
        local(f'tar -cvzf versions/{archive} web_static')

        return f'versions/{archive}'
    except Exception:
        return None


def deploy():
    arch_path = do_pack()
    if not arch_path:
        return False
    return do_deploy(arch_path)
