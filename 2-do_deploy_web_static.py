#!/usr/bin/python3
"""Script that distributes an archive to your web servers, using the
function do_deploy
"""
from fabric.api import task, run, put, env
from datetime import datetime as dt
import os


env.hosts = ['100.27.5.167', '54.157.180.169']


@task
def do_deploy(archive_path):
    """Distributes archive to web servers"""
    if not os.path.exists(archive_path):
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

    commands = f"""
    if [ ! -e "/tmp/" ]; then
        mkdir  -p "/tmp/";
        if [! -e "/tmp/" ]; then
            exit 1;
        fi
    fi

    if ls /data/web_static/releases/web_static* > /dev/null 2>&1
    then
        rm -rf /data/web_static/releases/web_static*;
    fi

    if ! mkdir -p /data/web_static/releases/{archive_folder} > \
        /dev/null 2>&1; then
        exit 1;
    fi

    if ! tar -xzf /tmp/{archive_name} -C \
        /data/web_static/releases/{archive_folder} > /dev/null 2>&1; then
        exit 1;
    fi

    if ! mv -f /data/web_static/releases/{archive_folder}/web_static/* \
        /data/web_static/releases/{archive_folder}/ > /dev/null 2>&1; then
        exit 1;
    fi

    if ! rm -rf /data/web_static/releases/{archive_folder}/web_static/ \
        > /dev/null 2>&1; then
        exit 1;
    fi

    if ! rm -rf /tmp/{archive_name} > /dev/null 2>&1; then
        exit 1;
    fi

    if [ -e "/data/web_static/current" ]
    then
        if ! rm -rf /data/web_static/current > /dev/null 2>&1; then
            exit 1;
        fi
    fi

    if ! ln -s /data/web_static/releases/{archive_folder} \
        /data/web_static/current > /dev/null 2>&1; then
        exit 1;
    fi
    """

    if run(commands).failed:
        return False

    return True
