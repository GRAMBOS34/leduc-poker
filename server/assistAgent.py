import numpy as np

#Deadass this file is just a modified file from the original rlcard library
class RandomAgent(object):
    ''' A random agent. Random agents is for running toy examples on the card games
    '''

    def __init__(self, num_actions):
        ''' Initilize the random agent

        Args:
            num_actions (int): The size of the ouput action space
        '''
        self.use_raw = False
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        return np.random.choice(list(state['legal_actions'].keys()))

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''

        self.num_actions = len(state['legal_actions'])

        probs = [0 for _ in range(self.num_actions)]
        for i in state['legal_actions']:
            probs[i - 1] = 1/len(state['legal_actions'])

        info = {}
        info['probs'] = {state['raw_legal_actions'][i]: probs[1 - (list(state['legal_actions'].keys())[i])] for i in range(len(state['legal_actions']))}

        return self.step(state), info