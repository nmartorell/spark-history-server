# This file is the actual code for the Python runnable build-shs-docker-image
from dataiku.runnables import Runnable

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
        spark_image = self.config["spark-base-image"]
        
        dockerfile = """
            FROM {0}

            USER root
            COPY entrypoint.sh /home/dataiku/
            RUN chown dataiku:dataiku /home/dataiku/entrypoint.sh \
                && chmod +x /home/dataiku/entrypoint.sh

            USER dataiku
            ENTRYPOINT ["/home/dataiku/entrypoint.sh"]""".format(spark_image)
        
        
        raise Exception("unimplemented")
        