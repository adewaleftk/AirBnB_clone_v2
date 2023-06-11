from fabric.api import env, put, run
import os


env.hosts = ['<IP web-01>', 'IP web-02']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.
    
    Args:
        archive_path: The path of the archive to deploy.
        
    Returns:
        True if all operations have been done correctly, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    
    archive_name = os.path.basename(archive_path)
    archive_folder = "/data/web_static/releases/{}".format(
        archive_name.split('.')[0]
    )
    
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, archive_folder))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))
        run("rm -rf {}/web_static".format(archive_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_folder))
        print("New version deployed!")
        return True
    except:
        return False

