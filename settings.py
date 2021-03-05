import yaml

with open("config.yaml") as file:
    config = yaml.safe_load(file)
db_conf = config["database"]
log_conf = config["logging"]
