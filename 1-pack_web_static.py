from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    
    All files in the folder web_static are added to the final archive.
    All archives are stored in the folder versions (the function creates this folder if it doesn’t exist).
    The name of the archive created follows the format web_static_<year><month><day><hour><minute><second>.tgz.
    
    Returns:
        The path of the generated archive if successful, None otherwise.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path), capture=True)

    if result.succeeded:
        return archive_path
    else:
        return None

