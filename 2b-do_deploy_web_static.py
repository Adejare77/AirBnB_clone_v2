#!/usr/bin/python3
"""Script that distributes an archive to your web servers, using the
function do_deploy
"""
from fabric.api import task, run, env, cd, put
from datetime import datetime as dt
import os


env.hosts = ['100.27.5.167', '54.157.180.169']


@task
def do_deploy(archive_path):
    """Distributes an archive to your web servers
    Args:
    archive_path: Path to the archive file to be distributed

    Return:
        False if no archive found, else True
    """

    # checks if the archive_path exists
    if os.path.isfile(archive_path) is False:
        return False

    """
    Rashisky: versions/web_static..., is a local path to the actual file
    web_static.... So, versions/ wouldn't be uploaded but, the actual
    file "web_static..." will be. Thus, the need to create archive_name
    """
    archive_name = archive_path.split("/")[-1]

    # archive_name without extension
    archive_folder = archive_name.split(".")[0]

    # upload local file to remote sever
    if put(archive_path, '/tmp/').failed:
        return False

    if run(f'rm -rf /data/web_static/releases/{archive_folder}').failed:
        return False

    # Creates the archive folder
    with cd('/data/web_static/releases/'):
        if run(f'mkdir {archive_folder}').failed:
            return False

    # extract archive to the created archive folder
    if not run(f'tar -xzf /tmp/{archive_name} -C \
               /data/web_static/releases/{archive_folder}').succeeded:
        return False

    # move all files inside archive_folder/web_static to archive folder
    with cd(f'/data/web_static/releases/{archive_folder}/'):
        if not run(f'mv web_static/* .').succeeded:
            return False

    # remove the archive_folder/web_static
    with cd(f'/data/web_static/releases/{archive_folder}/'):
        if not run(f'rm -r web_static').succeeded:
            return False

    # remove the archive file
    with cd('/tmp/'):
        if not run(f'rm -rf {archive_name}').succeeded:
            return False

    if run('rm -rf /data/web_static/current').failed:
        return False

    # Create a new link file "current"
    if run(f'ln -s /data/web_static/releases/{archive_folder} \
           /data/web_static/current').failed:
        return False

    return True
