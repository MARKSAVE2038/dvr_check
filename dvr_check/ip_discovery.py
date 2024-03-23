import requests
import json
from pathlib import Path

from datetime import datetime

CACHE_FILE = ".cache"

def find_public_ip() -> str:
    response = requests.get("https://api.ipify.org?format=json")
    response.raise_for_status()

    return response.json()['ip']

def update_cache(value) -> bool:
    cache_file = Path(CACHE_FILE).resolve()

    try:
        last_data = json.loads(cache_file.read_text())["data"]["publicIP"]
    except:
        last_data = ""
    
    if last_data == value:
        print(f"INFO: Value has not changed, cache is still valid")
        return False
    
    print(f"INFO: Updating last cached data with '{value}'")
    cache_file.write_text(json.dumps({
        "metadata": {
            "lastUpdate": datetime.today().isoformat()
        },
        "data": {
            "publicIP": value
        }
    }, indent=4))
    return True
