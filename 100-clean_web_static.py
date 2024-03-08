#!/usr/bin/python3
'''Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean'''
from fabric.api import run, env, local, cd, lcd


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    '''clean'''
    number = int(number)
    try:
        # context manger for local
        with lcd('versions/'):
            versions = local('ls -t versions/', capture=True).split()
            versions = versions[1:] if number <= 1 else versions[number:]
            for v in versions:
                local(f'rm -rf versions/{v}')

        # context manger for remote
        with cd('/data/web_static/releases'):
            releases = run('ls -t /data/web_static/releases').split()
            rels = releases[1:] if number <= 1 else releases[number:]
            for rel in rels:
                run(f'rm -rf /data/web_static/releases/{rel}')

    except Exception:
        pass
