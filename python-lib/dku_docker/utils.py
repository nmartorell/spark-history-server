def generate_entrypoint_command(config):
    """
    Generate command for entrypoint based on cloud storage selected.
    """
    
    cloud_storage = config["cloud_storage"]
    if cloud_storage == "s3":
        aws_access_key = config["aws_access_key"]
        aws_secret_key = config["aws_secret_key"]
        s3_events_dir = 
        
        
    elif cloud_storage == "wasbs":
        
    elif cloud_storage == "gcs":
        raise Unimplemented
    else:
        raise Exception("this shouldn't happen.")