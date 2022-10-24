import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from src.utils.mongo_operations import race_data_to_mongo, drivers_data_to_mongo
from src.utils.mongo_operations import cicuits_data_to_mongo, raceresults_data_to_mongo
import random
import pymongo
import json
import requests

STAGE = "Get Data"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path, params_path, secrets_path):
    ## reading config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    secrets = read_yaml(secrets_path)

    conn_str = secrets["mongodb"]["url"].format(secrets["mongodb"]["username"],secrets["mongodb"]["pwd"])
    print(conn_str)
    mclient = pymongo.MongoClient(conn_str)


    race_data_to_mongo(conn_str,mclient,config)
    drivers_data_to_mongo(conn_str,mclient,config)
    cicuits_data_to_mongo(conn_str,mclient,config)
    raceresults_data_to_mongo(conn_str,mclient,config)




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--secrets", "-s", default="configs/secrets.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params, secrets_path=parsed_args.secrets)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e