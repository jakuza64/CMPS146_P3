
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
    pass

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
            return node #,state
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
    return node.child_nodes[next_action]#, state
    pass
    # Hint: return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    moves = state.legal_moves
    for move in moves:
        for r in range(num_nodes):
                rollout_state = state.copy()
                rollout_state.apply_move(move)
    
                # Only play to the specified depth. (estimated max 24 moves possible)
                for i in range(50):
                    if rollout_state.is_terminal():
                        break
                    rollout_move = choice(rollout_state.legal_moves)
                    rollout_state.apply_move(rollout_move)
    
               #total_score += outcome(rollout_state.score)
            
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while(node.parent != None):
        if(won):
            node.wins += 1;
        node = node.parent
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

        #Traversal (Find leaf nodes)
        #leaf,state = traverse_nodes(node, state, identity_of_bot)
        leaf = traverse_nodes(node, sampled_game, identity_of_bot)


        #Expansion (Add new node with unexplored action)
        #new_node,state = expand_leaf(leaf,state)
        new_node = expand_leaf(leaf,sampled_game)


        #Rollout (Simulate remainder of game)
        rollout(sampled_game)
        

        #Backpropagate (Send result back up tree)
        backpropagate(new_node, new_node.wins)
        

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    highest_win_rate = None
    best_node = None
    for n in root_node.child_nodes:
        if(n.wins/n.visits) > highest_win_rate:
            highest_win_rate = n.wins/n.visits
            best_node = n
    return best_node.parent_action
