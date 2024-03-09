#!/usr/bin/python3
'''script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy

Attrs:
    env: enviroment variables for fabric
'''
from fabric.api import run, put, env, sudo, task
from os.path import exists
do_pack = __import__('1-pack_web_static').do_pack


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']
env.key_filename = '~/.ssh/school'


@task(default=True)
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
        run(f'tar -xzf /tmp/{archive}.tgz -C {target}')
        run(f'rm /tmp/{archive}.tgz')
        run(f'mv {target}/web_static/* {target}')
        run(f'rm -rf {target}/web_static')
        # remove symbolic link
        run('rm -rf /data/web_static/current')
        # create new link
        run(f'ln -s {target} /data/web_static/current')

        return True
    except Exception:
        return False
