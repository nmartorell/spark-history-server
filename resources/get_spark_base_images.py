import dataiku
import docker

def do(payload, config, plugin_config, inputs):
    
    # get docker client
    docker_client = docker.from_env()
    
    # get spark base images -- assumes spark images have been downloaded from our cdn
    spark_image_tags = list()
    for img in docker_client.images.list("dataiku-dss-spark-exec-base"):
        spark_image_tags.append(next(x for x in img.tags if "dataiku-dss-spark-exec-base" in x))

    return [{"label":tag, "value":tag} for tag in spark_image_tags]