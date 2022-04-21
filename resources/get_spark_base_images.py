import dataiku
import docker

def do(payload, config, plugin_config, inputs):
    
    # get docker client
    