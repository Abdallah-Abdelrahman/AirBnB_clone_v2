#!/usr/bin/python3
'''Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean'''
from fabric.api import run, env, local
from os import listdir


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    '''clean'''
    res = listdir('versions')
    number = int(number)
    versions = res[1:] if (number) <= 1 else res[number:]
    # get archives sort from most recents
    releases = run('ls -t /data/web_static/releases').strip().split()
    rels = releases[1:] if (number) <= 1 else releases[number:]

    for v in versions:
        local(f'rm -rf versions/{v}')
    for rel in rels:
        run(f'rm -rf /data/web_static/releases/{rel}')
