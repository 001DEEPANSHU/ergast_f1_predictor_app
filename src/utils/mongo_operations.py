import requests
import pymongo
import logging
import json
import pandas as pd


def race_data_to_mongo(conn_str, mclient,config):
    """ 
    Function to get races data from Ergast API and write the data to Mongo DB collection

    """
    seasons = requests.get(config["source_data"]["url"])
    f1_seasons = json.loads(seasons.text)["MRData"]["SeasonTable"]["Seasons"]

    try:
        db = mclient.Ergast_F1
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


def drivers_data_to_mongo(conn_str, mclient,config):
    """ 
    Function to get drivers' data from Ergast API and write the data to Mongo DB collection

    """
    seasons = requests.get(config["source_data"]["url"])
    f1_seasons = json.loads(seasons.text)["MRData"]["SeasonTable"]["Seasons"]


    try:
        db = mclient.Ergast_F1
        collection = db.drivers
        d_obj = requests.get(f"https://ergast.com/api/f1/drivers.json?limit=1000")
        drivers = json.loads(d_obj.text)["MRData"]["DriverTable"]["Drivers"]
        logging.info(f"Started: Drivers data transfer to Mongo DB")
        for i in drivers:
            collection.insert_one(i)
        
        logging.info(f"Completed: Drivers' data transfer to Mongo DB")

    except Exception as e: 
        print('Error encountered: '+ str(e))      




def cicuits_data_to_mongo(conn_str, mclient,config):
    """ 
    Function to get Circuits data from Ergast API and write the data to Mongo DB collection

    """
    seasons = requests.get(config["source_data"]["url"])
    f1_seasons = json.loads(seasons.text)["MRData"]["SeasonTable"]["Seasons"]


    try:
        db = mclient.Ergast_F1
        collection = db.circuits
        c_obj = requests.get(f"https://ergast.com/api/f1/circuits.json?limit=1000")
        circuits = json.loads(c_obj.text)["MRData"]["CircuitTable"]["Circuits"]
        logging.info(f"Started: Circuits' data transfer to Mongo DB")
        for i in circuits:
            collection.insert_one(i)
        logging.info(f"Completed: Circuits' data transfer to Mongo DB")

    except Exception as e: 
        print('Error encountered: '+ str(e)) 



def raceresults_data_to_mongo(conn_str, mclient,config):

    """ 
    Function to get Race result's data from Ergast API and write the data to Mongo DB collection

    """
    seasons = requests.get(config["source_data"]["url"])
    f1_seasons = json.loads(seasons.text)["MRData"]["SeasonTable"]["Seasons"]


    try:
        db = mclient.Ergast_F1
        collection = db.results
        
        logging.info(f"Started: Race results data transfer to Mongo DB")
        for season in f1_seasons:
            season_results = requests.get(f"http://ergast.com/api/f1/{season['season']}/results.json?limit=1000")
            races = json.loads(season_results.text)["MRData"]["RaceTable"]["Races"]
            
            for i in races:
                collection.insert_one(i)
                
        logging.info(f"Completed: Race results data transfer to Mongo DB")

    except Exception as e: 
        print('Error encountered: '+ str(e)) 


def data_from_mongo(conn_str, mclient,config):

    db = mclient.Ergast_F1
    collection = db.results
    race_results = list(collection.find({}))

    result_dict = {'Season':[],'Round':[],'Race Name':[],'Race Date':[],'Race Time':[],'Position':[],
                     'Points':[],'Grid':[],'Laps':[],'Status':[],'Driver':[],'DOB':[],
                     'Nationality':[],'Constructor':[],'Constructor Nat':[],'Circuit Name':[],'Race Url':[],
                     'Lat':[],'Long':[],'Locality':[],'Country':[]}

    for race in race_results:
        for results in race['Results']:
            result_dict['Season'].append(f"{race['season']}")
            result_dict['Round'].append(int(race['round']))
            result_dict['Race Name'].append(f"{race['raceName']}")
            result_dict['Race Date'].append(f"{race['date']}")
            result_dict['Race Time'].append(f"{race['time']}" if 'time' in results else '10:10:00Z')
            result_dict['Position'].append(int(results['position']))
            result_dict['Points'].append(float(results['points']))
            result_dict['Grid'].append(int(results['grid']))
            result_dict['Laps'].append(int(results['laps']))
            result_dict['Status'].append(f"{results['status']}")
            result_dict['Driver'].append(f"{results['Driver']['givenName']} {results['Driver']['familyName']}")
            result_dict['DOB'].append(f"{results['Driver']['dateOfBirth']}")
            result_dict['Nationality'].append(f"{results['Driver']['nationality']}")
            result_dict['Constructor'].append(f"{results['Constructor']['name']}")
            result_dict['Constructor Nat'].append(f"{results['Constructor']['nationality']}")
            result_dict['Circuit Name'].append(f"{race['Circuit']['circuitName']}")
            result_dict['Race Url'].append(f"{race['url']}")
            result_dict['Lat'].append(f"{race['Circuit']['Location']['lat']}")
            result_dict['Long'].append(f"{race['Circuit']['Location']['long']}")
            result_dict['Locality'].append(f"{race['Circuit']['Location']['locality']}")
            result_dict['Country'].append(f"{race['Circuit']['Location']['country']}")

    result_df = pd.DataFrame(result_dict)
    return result_df
    
