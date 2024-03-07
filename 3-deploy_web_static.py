#!/usr/bin/python3
'''Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy'''


def deploy():
    arch_path = __import__('1-pack_web_static').do_pack()
    if not arch_path:
        return False
    return __import__('2-do_deploy_web_static').do_deploy(arch_path)
