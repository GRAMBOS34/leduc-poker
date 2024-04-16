import rlcard
from assistAgent import RandomAgent  # Replace with your desired agent
from collections import OrderedDict

def get_agent_suggestion(state):
    """
    Creates an environment, agent, and returns a suggested action for Leduc hold'em poker based on a given state.

    Args:
        state (dict): The current game state representation.

    Returns:
        int: The suggested action by the agent.
    """

    # Create the Leduc hold'em environment (closed within the function)
    env = rlcard.make('leduc-holdem')

    # Create an agent (consider adjusting hidden layers as needed)
    agent = RandomAgent(env.action_shape)

    # Get the suggested action based on the state
    action = agent.eval_step(state)

    # Clean up the environment
    #env.close()

    # Access the second element (dictionary)
    probs_dict = action[1]

    # Access the "probs" key within the dictionary (which is an OrderedDict)
    suggestedAction = list(probs_dict['probs'])[action[0] - 1]

    return suggestedAction