import requests
import pymongo
import logging
import json


def race_data_to_mongo(conn_str, connect,config):
    """ 
    Function to get races data from Ergast API and write the data to Mongo DB collection

    """
    seasons = requests.get(config["source_data"]["url"])
    f1_seasons = json.loads(seasons.text)["MRData"]["SeasonTable"]["Seasons"]

    try:
        db = connect.Ergast_F1
        collection = db.races
        logging.info(f"Started: Races data transfer to Mongo DB")
        
        for season in f1_seasons:
            race_schedule = requests.get(f"http://ergast.com/api/f1/{season['season']}.json")
            races = json.loads(race_schedule.text)["MRData"]["RaceTable"]["Races"]
            for race in races:
                collection.insert_one(race)
        logging.info(f"Completed: Races data transfer to Mongo DB")

    except Exception as e:
        logging.info(f'Error encounterd: '+ str(e))
