import rlcard
from rlcard import models
from botAgent import HumanAgent
from rlcard.utils import print_card
from updateJsonFile import update_json_file
from updateJsonFile import get_action
import json

# Make environment
env = rlcard.make('leduc-holdem')
human_agent = HumanAgent(env.num_actions)
cfr_agent = models.load('leduc-holdem-cfr').agents[0]
env.set_agents([
    human_agent,
    cfr_agent,
])

FILENAME = 'server/state.json'

def newRound() -> bool:
    try:
        with open(FILENAME, "r+") as file:
            data = json.load(file)
            if data["newRound"] == True:
                return True
            else: return False
    
    except:
        newRound()

while True:
    update_json_file(FILENAME, key="newRound", new_value=False)
    update_json_file(FILENAME, key="action", new_value=None)

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    final_state = trajectories[0][-1]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])

    #Shows the opening move (by the bot)
    for pair in _action_list:
        print('>> Agent', pair[0], 'chooses', pair[1])

    # Let's take a look at what the agent card is
    print('===============     CFR Agent    ===============')
    print_card(env.get_perfect_information()['hand_cards'][1])
    update_json_file(filename=FILENAME, key='bot_card', new_value=(list(env.get_perfect_information()['hand_cards'][1])))

    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win {} chips!'.format(payoffs[0]))
        update_json_file(filename=FILENAME, key='result', new_value="win")
        update_json_file(filename=FILENAME, key='reward', new_value=(payoffs[0]))
    elif payoffs[0] == 0:
        print('It is a tie.')
        update_json_file(filename=FILENAME, key='result', new_value="draw")
        update_json_file(filename=FILENAME, key='reward', new_value=(0))
    else:
        print('You lose {} chips!'.format(-payoffs[0]))
        update_json_file(filename=FILENAME, key='result', new_value="loss")
        update_json_file(filename=FILENAME, key='reward', new_value=(payoffs[0]))

    print('') 
    print(action_record)

    
    #so it'll start the next round for the bot
    while not newRound():
        newRound()

    # inputs = input("Press any key to continue, Q to exit\n")
    # if inputs.lower() == "q":
    #     break
