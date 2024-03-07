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
    if not os.path.exists(archive_path):
        return False
    try:
        """
        Rashisky: versions/web_static..., is a local path to the actual file
        web_static.... So, versions/ wouldn't be uploaded but, the actual
        file "web_static..." will be. Thus, the need to create archive_name
        """
        archive_name = archive_path.split("/")[-1]

        # archive_name without extension
        archive_folder = archive_name.split(".")[0]

        # check if "/tmp" exists, if not create one
        create_dir = """
        if [ ! -e "/tmp/" ]
        then
            mkdir  -p "/tmp/";
        fi
        """
        run(create_dir)

        # upload local file to remote sever
        put(archive_path, '/tmp/')

        commands = f"""
        mkdir -p /data/web_static/releases/{archive_folder};

        tar -xzf /tmp/{archive_name} -C \
            /data/web_static/releases/{archive_folder};

        mv -f /data/web_static/releases/{archive_folder}/web_static/* \
            /data/web_static/releases/{archive_folder}/;

        rm -r /data/web_static/releases/{archive_folder}/web_static/;

        rm -rf /tmp/{archive_name};

        rm -rf /data/web_static/current;

        sudo ln -s /data/web_static/releases/{archive_folder} \
            /data/web_static/current;
        """

        run(commands)

        return True

    except Exception as e:
        return False