import base64
from xxlimited import Str
import httpx
import json
import questionary
import sys
from pprint import pp
from pathlib import Path

base_url = "https://events.critelli.technology"
puzzle_goes_here = Path("/Users/Nora/Library/Application Support/Opus Magnum/76561198361444248/custom/")

def main():
    timeframe = is_oki(base_url)
    time = questionary.select("View Collections?", choices=timeframe.keys()).ask()
    collections = {i["collectionName"] : i for i in timeframe[time]}
    pp(collections)
    collection = collections[
            questionary.select(">",
                               choices=collections.keys()).ask()
            ]
    print(collection)
    events = {i["title"] : i for i in collection['events']}
    pp(events)
    event = events[questionary.select(collection["collectionName"], choices=events.keys()).ask()]
    puzzle = is_oki(event["url"])
    with open(puzzle_goes_here / puzzle['puzzleFileName'], 'wb') as f:
        f.write(base64.b64decode(puzzle['puzzleFileBase64']))



def is_oki(url):
    match (response := httpx.get(url, headers={"Accept": "application/json"})).status_code:
        case 200:
            return json.loads(response.read())
        case _:
            print("idk something broke", file=sys.stderr)
            print(response)
            exit(1)


if __name__ == "__main__":
    main()
