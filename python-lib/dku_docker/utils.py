def generate_entrypoint_command(config):
    """
    Generate command for entrypoint based on cloud storage selected.
    """
    
    cloud_storage = config["cloud_storage"]
    if cloud_storage == "s3":
        
    elif cloud_storage == "wasbs":
        
    elif cloud_storage == "gcs":
        
    else:
        raise Exception("this shouldn't happen")