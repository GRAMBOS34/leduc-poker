import json

previousUpdate = {}

#made this into a module since i use it so much
def update_json_file(filename, key, new_value):
    global previousUpdate
    try:
        with open(filename, 'r+') as file:
            # Load data from JSON file
            data = json.load(file)
            previousUpdate = data

            # Update the value in the dictionary
            if key in data:
                data[key] = new_value
            else:
                print(f"Key '{key}' not found in '{filename}'.")

            # Create an empty dictionary if data is empty
            if not data:
                new_data = {}
            else:
                new_data = data  # Use existing data if present
            
            # Write the empty/updated dictionary
            json.dump(new_data, file, indent=4)

            # Clear the file content
            file.truncate(0)
            file.seek(0)

            # Write the updated dictionary back to the file
            json.dump(data, file, indent=4)
            print(f"Value for key '{key}' updated in '{filename}'.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")

def check_update(filename):
    global previousUpdate
    while True:
        with open(filename, 'r') as f:
            try:
                state = json.load(f)

                if state == previousUpdate: 
                    return False
                
                if state["actionRepeat"] == True:
                    update_json_file(filename=filename, key='actionRepeat', new_value=False)
                    return True
            
                previousUpdate = state
                return True
            
            except: 
                continue
    

def get_action(filename):
    """
    Reads the player's action from a JSON or text file.

    Args:
        filename (str): Path to the file containing the action.

    Returns:
        int: The player's action (index in the action space).
    """

    global previousUpdate

    while check_update(filename=filename) == False:
        continue

    try:
        with open(filename, 'r') as f:
            if filename.endswith('.json'):  # Check for JSON file
                action_data = json.load(f)
                previousUpdate = action_data['action']
                print(action_data['action'])

                if action_data['action'] == 'call':
                    try:
                        return action_data['state']['legal_actions'].index(action_data['action'])
                    
                    except:
                        return action_data['state']['legal_actions'].index('check')
                    
                if action_data['action'] == 'raise':
                    try:
                        return action_data['state']['legal_actions'].index(action_data['action'])
                    
                    except:
                        return action_data['state']['legal_actions'].index('bet')
                    
                return action_data['state']['legal_actions'].index(action_data['action'])
                
            else:  # Assume text file with action on a single line
                action_string = f.read().strip()
                return int(action_string)
    except ValueError:
        return None  # Or handle the error differently