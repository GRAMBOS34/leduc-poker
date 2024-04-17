#literally just does what the file name says
#i am not sugarcoating this just run this to reset the data.json
import json

resetState = {
    "fold": 0,
    "check": 0,
    "raise": 0,
    "win": 0,
    "loss": 0,
    "draw": 0,
    "suggestionTaken": 0,
    "suggestionIgnored": 0
}

with open('server/data.json', "r+") as file:
    data = json.load(file)

    data = resetState

    file.truncate(0)
    file.seek(0)

    json.dump(data, file, indent=4)