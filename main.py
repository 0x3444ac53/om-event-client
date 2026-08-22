import base64
import httpx
import json
import questionary
import sys
from platform import system
from pathlib import Path


base_url = "https://events.critelli.technology"

match system(): # System Specific Save Dir
    case "Windows":
        puzzle_goes_here = Path.home() / Path("Documents/My Games/Opus Magnum")
    case "Darwin":
        puzzle_goes_here = Path.home() / Path("Library/Application Support/Opus Magnum")
    case "Linux":
        puzzle_goes_here = Path.home() / Path(".local/share/Opus Magnum")
    case _:
        raise RuntimeError("The fuck is your OS???")

# find NUMBERS
puzzle_goes_here /= [i for i in puzzle_goes_here.iterdir() if i.name.isdigit()][0] / "custom"


def main():
    timeframe = is_oki(base_url)
    time = questionary.select("View Collections?", choices=timeframe.keys()).ask()
    collections = {i["collectionName"] : i for i in timeframe[time]}
    collection = collections[
            questionary.select(">",
                               choices=collections.keys()).ask()
            ]
    events = {i["title"] : i for i in collection['events']}
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
