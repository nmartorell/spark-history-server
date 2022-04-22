def generate_entrypoint_command(config):
    """
    Generate command for entrypoint based on cloud storage selected.
    """
    
    cloud_storage = config["cloud_storage"]
    if cloud_storage == "s3":       
        # extract config values
        aws_access_key = config["aws_access_key"]
        aws_secret_key = config["aws_secret_key"]
        s3_events_dir = config["s3_events_dir"]
        
        # generate command
        command = "--{0} false {1} {2} --events-dir s3a://{3}".format(cloud_storage, aws_access_key, aws_secret_key, s3_events_dir)
        
    elif cloud_storage == "wasbs":
        # extract config values 
        
        
        # generate command
        
    elif cloud_storage == "gcs":
        raise Exception("unimplemented")
    else:
        raise Exception("This shouldn't happen... invalid Cloud Storage.")
        
    return command