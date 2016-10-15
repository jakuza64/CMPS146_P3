
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def get_urgent_child(node,identity):
    n = node.visits
    maxUCB = 0
    best_child = None
    for action,child in node.child_nodes.items():
        xj = child.wins/child.visits
        # If opponent
        if identity != state.player_turn:
            xj = 1 - xj
        nj = child.visits

        # Calculate
        newUCB = xj + explore_faction * (sqrt((2 * log(n)) / (nj)))
        if newUCB > maxUCB:
            best_child = child
            maxUCB = newUCB

    #If none, current node is leaf node
    return best_child


def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    while True:
        next_node = get_urgent_child(node,identity)
        if next_node != None:
            state.apply_move(next_node.parent_action)
            node = next_node
        else:
            return node,state
    pass
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    next_action = node.untried_actions.pop()
    next_node = MCTSNode(parent=node, parent_action=next_action, action_list=node.untried_actions)
    node.child_nodes[next_action] = next_node
    state.apply_move
    return node.child_nodes[next_action], state
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    pass


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = state.player_turn
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

        #Traversal
        leaf,state = traverse_nodes(node, state, identity_of_bot)

        #Expansion
        new_node,state = expand_leaf(leaf,state)

        #Rollout

        #Backpropagate

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
