# This file is the actual code for the Python runnable build-shs-docker-image
from dataiku.runnables import Runnable
from dku_docker.templates import entrypoint, dockerfile

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
        
    def get_progress_target(self, percent):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return (percent, "NONE")

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        # get spark image name, and dss version, from config
        spark_image = self.config["spark-base-image"]
        dss_version = spark_image.split(":")[1]
        
        # generate dockerfile from template
        dockerfile = dockerfile.format(spark_image)
        
        # write dockerfile and entrypoint.sh to tmp directory
        tmp_folder = "/tmp/shs-docker-env/"
        os.mkdir(tmp_folder)
        
        f = open(tmp_folder+"dockerfile", mode="w")
        f.writelines(dockerfile)
        f.close()
        
        f = open(tmp_folder+"entrypoint.sh", mode="w")
        f.writelines(entrypoint)
        f.close()
        
        # build shs base image
        docker_client = docker.from_env()
        docker_client.images.build(path=tmp_folder, tag="spark-history-server:{}".format(dss_version))
        
        # remove tmp folder
        shutil.rmtree(tmp_folder)
        
        # return fake percentage progress - 50%
        self.get_progress_target(50)
        
        # start spark history server -- use dummy vars for now, need to build command later
        s3_access_key = "AKIAUKG7R5HWVTOYGSYF"
        s3_secre_key = "4ENpGUzf6CisQidY1aS+nowIFBBwaYdH/eKJlmyx"
        events_dir = "ned-martorell/shs"
        
        command = "--s3 false {0} {1} --events-dir s3a://{2}".format(s3_access_key, s3_secret_key, events_dir)
        docker_client.
        
        # return fake percentage progress - 100%
        self.get_progress_target(100)
        
        return None #TODO: return image name
        