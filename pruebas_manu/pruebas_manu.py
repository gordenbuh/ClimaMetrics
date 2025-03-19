import os
import json
import requests
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger("AEMET API")


try:
    with open('pruebas_manu\credentials.json') as data:
        credentials = json.load(data)
        API_KEY = credentials['AEMET_API_Key']
        logger.info("Credentials  loaded successfully") 
except FileNotFoundError:
    logger.error("credential.json file not found")
    raise
except json.JSONDecodeError:
    logger.error("credentials.json is not a valid JSON file")
    raise
except KeyError:
    logger.error("AEMET_API_KEY not found in the credentials file")
    raise

headers = {
        "api_key": API_KEY,
    }
area="p"
endpoint=f"https://opendata.aemet.es/opendata/api/incendios/mapasriesgo/estimado/area/{area}"

try:
    logger.info("Making request")
    aemet_response=requests.get(endpoint, headers=headers)
    
    if aemet_response.status_code == 200:
        logger.info("Data received successfully")
        data = aemet_response.json()

        if "datos" in data:
            logger.info(f"Fetching data from: {data['datos']}")
            opendata_response=requests.get(data["datos"])
            
            if opendata_response.status_code==200:
                opendata_data = opendata_response.json()
                
                current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"fire_risk_data_{area}_{current_date}.json"

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(opendata_data, f, ensure_ascii=False, indent=4)
                
                logger.info(f"Data saved to file: {filename}")
                
except Exception as e:
    logger.error(f"Error:{e}")
    raise e

