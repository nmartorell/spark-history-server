# This file is the actual code for the Python runnable build-shs-docker-image
from dataiku.runnables import Runnable
from dku_docker.templates import dockerfile_template, entrypoint
from dku_docker.utils import generate_entrypoint_command

import os
import shutil
import docker

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        # get spark image name, and dss version, from config
        spark_image = self.config["spark-base-image"]
        dss_version = spark_image.split(":")[1]
        
        # generate dockerfile from template
        dockerfile = dockerfile_template.format(spark_image)
        
        # write dockerfile and entrypoint.sh to tmp directory
        tmp_folder = "/tmp/shs-docker-env/"
        try:
            shutil.rmtree(tmp_folder)
        except:
            pass
        finally:
            os.mkdir(tmp_folder)
        
        f = open(tmp_folder+"dockerfile", mode="w")
        f.writelines(dockerfile)
        f.close()
        
        f = open(tmp_folder+"entrypoint.sh", mode="w")
        f.writelines(entrypoint)
        f.close()
        
        # build shs base image
        docker_client = docker.from_env()
        shs_image_tag = "spark-history-server:{0}".format(dss_version)
        shs_image_obj, _ =  docker_client.images.build(path=tmp_folder, tag=shs_image_tag)
        
        # remove tmp folder
        shutil.rmtree(tmp_folder)
        
        # check if the spark history server is already running for this image -- if so, exit
        for container in docker_client.containers.list():
            for tag in container.image.tags:
                if shs_image_tag.split(":")[0] in tag:
                    return "Spark History Server already started. Please stop before restarting."
        
        # start spark history server 
        port = self.config["port"]
        command = generate_entrypoint_command(self.config)
        
        docker_client.containers.run(image=shs_image_obj.id, 
                                     ports={'18080/tcp': port},
                                     command=command,
                                     detach=True)
        
        return "Spark History Server successfully started on port {0}".format(port)
        