#!/usr/bin/python3
'''script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy

Attrs:
    env: enviroment variables for fabric
'''
from fabric.api import local, put, env, sudo, runs_once
from os.path import exists, basename
from datetime import datetime


env.user = 'ubuntu'
env.hosts = ['52.91.118.253', '35.153.16.72']
env.key_filename = '~/.ssh/school'


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


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Uncompress the archive to the folder /data/web_static/releases/
        archive_name = basename(archive_path)
        archive_name_no_ext = archive_name.split(".")[0]
        sudo("mkdir -p /data/web_static/releases/{}/".format(
            archive_name_no_ext
            ))
        sudo(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_name, archive_name_no_ext
            )
        )
        # Copy the contents of web_static to the parent directory
        sudo("rsync -a /data/web_static/releases/{}/web_static/ "
             "/data/web_static/releases/{}/".format(
                archive_name_no_ext, archive_name_no_ext
                )
             )
        # Remove the now empty web_static directory
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(
            archive_name_no_ext
        ))
        # Delete the archive from the web server
        sudo("rm -rf /tmp/{}".format(archive_name))
        # Delete the symbolic link /data/web_static/current from the web server
        sudo("rm -rf /data/web_static/current")
        # Create a new the symbolic link /data/web_static/current on server
        # linked to the new version of your code
        sudo(
            "ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(
                archive_name_no_ext
            )
        )
        print("New version deployed!")
        return True
    except Exception:
        return False
