#!/usr/bin/python3
'''Module Fabric script that generates a .tgz archive.
from the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack'''
from fabric.api import local, runs_once
from datetime import datetime


@runs_once
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
