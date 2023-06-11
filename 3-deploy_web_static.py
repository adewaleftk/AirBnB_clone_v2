#!/usr/bin/python3
# Web static configuration file

"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """Creates a compressed archive of web_static contents"""
    try:
        local("mkdir -p versions")
        archive_name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
        path = "versions/" + archive_name
        local("tar -czvf {} web_static".format(path))
        return path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        put(archive_path, "/tmp/{}".format(filename))
        folder_name = "/data/web_static/releases/{}".format(filename.split(".")[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}/".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

