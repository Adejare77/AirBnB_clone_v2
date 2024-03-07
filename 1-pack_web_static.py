#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, using the function do_pack
"""
from fabric.api import task, local
from datetime import datetime as dt
import os


@task
def do_pack():
    """generate a .tgz archive"""
    try:
        # check if "version" directory exists
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Gets the current full date and time
        date = dt.now().strftime("%Y%m%d%H%M%S")

        # Archive full name
        archive_name = f'versions/web_static_{date}.tgz'

        # run locally and create a tgz file
        # c = create, f = filename, z = gzip, gunzip, ungzip compression
        # v = verbose
        local(f"tar -cvzf {archive_name} web_static/")

        return archive_name

    except Exception:
        return None
