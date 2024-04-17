from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from updateJsonFile import update_json_file

app = Flask(__name__)
CORS(app, resources={r'/update/*', r'/show/*', r'/action'})

#Total player statistics
wins = 0
losses = 0
draws = 0
suggestionsTaken = 0
suggestionsIgnored = 0
FILENAME = 'server/state.json'
callNum = 0

#Gets the action from the app
@app.route('/action', methods=["POST"])
def update_action():
  global callNum
  callNum += 1
  if callNum >= 2:
    action = request.json.get('action')
    with open(FILENAME, "r+") as file:
        data = json.load(file)

        data["action"] = action
        data["actionRepeat"] = True

        file.truncate(0)
        file.seek(0)

        json.dump(data, file, indent=4)

  else:
    action = request.json.get('action')
    with open(FILENAME, "r+") as file:
        data = json.load(file)

        data["action"] = action
        data["actionRepeat"] = True

        file.truncate(0)
        file.seek(0)

        json.dump(data, file, indent=4)

  return jsonify({"message": "Action successfully updated"})

@app.route('/update/new_round', methods=["POST"])
def newRound():
    state = request.json.get('action')
    with open(FILENAME, "r+") as file:
      data = json.load(file)

      data["newRound"] = state

      file.truncate(0)
      file.seek(0)

      json.dump(data, file, indent=4)

    return jsonify({"message": "Action successfully updated"})


@app.route('/show/all', methods=["GET"])
def show_all():
    stats = {
        "Total wins": wins,
        "Total losses": losses,
        "Total draws": draws,
        "Total suggestions taken": suggestionsTaken,
        "Total suggestions ignored": suggestionsIgnored
    }

    return jsonify(stats)

#*This is how we get data from the react file
"""
const update_win = async (win) => {
    try {
      const response = await fetch('http://localhost:5000/update/win', {
        method: 'POST',
        headers: { 'Content-type': 'application/json'},
        body: JSON.stringify({ win }), // Send updated value in JSON
      });
  
      if (response.ok) {
        console.log('Value updated successfully!');
      } else {
        console.error('Error updating value:', await response.text());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
"""

if __name__ == "__main__":
    app.run(debug=True)