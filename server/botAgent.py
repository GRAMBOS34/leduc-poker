from rlcard.utils.utils import print_card
from updateJsonFile import update_json_file
from updateJsonFile import get_action
from updateJsonFile import check_update
from assistBot import get_agent_suggestion

#file name for the json file that the bot, server, and website read off of 
#not the best way to do this but honestly i dont have much of a choice anymore
FILENAME = 'server/state.json'

#Deadass this file is just a modified file from the original rlcard library
class HumanAgent(object):
    ''' A human agent for Leduc Holdem. It can be used to play against trained models
    '''

    def __init__(self, num_actions):
        ''' Initilize the human agent

        Args:
            num_actions (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        suggestedAction = get_agent_suggestion(state)

        #updates the suggested action
        update_json_file(FILENAME, key='suggested_action', new_value=suggestedAction)

        _print_state(state['raw_obs'], state['action_record'])

        while not check_update(FILENAME):
            action = get_action(filename=FILENAME)
            print(state['raw_legal_actions'][action])

            return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        
        return self.step(state), {}

def _print_state(state, action_record):
    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the historical actions
    '''

    playerHand = list(state["hand"])
    try:
        publicCard = list(state["public_card"])
        update_json_file(filename=FILENAME, key="public_card", new_value=publicCard)
    
    except:
        update_json_file(filename=FILENAME, key="public_card", new_value=None)

    update_json_file(filename=FILENAME, key="state", new_value=state)
    update_json_file(filename=FILENAME, key="player_hand", new_value=playerHand)
    update_json_file(filename=FILENAME, key='bot_card', new_value=None)

    pot = sum(state["all_chips"])
    update_json_file(filename=FILENAME, key="pot", new_value=pot)
    update_json_file(filename=FILENAME, key='result', new_value=None)
    update_json_file(filename=FILENAME, key='reward', new_value=None)

    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])

    #Shows the moves of the bot during the game
    for pair in _action_list:
        print('>> Agent', pair[0], 'chooses', pair[1])
        update_json_file(filename=FILENAME, key="lastMoveAI", new_value=pair[1])

    print('\n=============== Community Card ===============')
    print_card(state['public_card'])
    print('===============   Your Hand    ===============')
    print_card(state['hand'])
    print('===============     Chips      ===============')
    print('Yours:   ', end='')
    for _ in range(state['my_chips']):
        print('+', end='')
    print('')
    for i in range(len(state['all_chips'])):
        if i != state['current_player']:
            print('Agent {}: '.format(i) , end='')
            for _ in range(state['all_chips'][i]):
                print('+', end='')
    print('\n=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + action for index, action in enumerate(state['legal_actions'])]))
    print('')