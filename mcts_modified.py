
from mcts_node import MCTSNode
from random import choice
from random import shuffle
from math import sqrt, log

num_nodes = 1000
explore_faction = .25

def get_urgent_child(node, state, identity):
    n = node.visits
    maxUCB = 0
    best_child = None
    for action,child in node.child_nodes.items():
        xj = child.wins/child.visits
        # If opponent
        if identity != state.player_turn:
            xj = 1 - xj
        nj = child.visits
        exploration_term = sqrt((2 * log(n)) / nj)
        # Calculate
        newUCB = xj + (explore_faction * exploration_term)
        if newUCB > maxUCB:
            best_child = child
            maxUCB = newUCB

    # If none, current node is leaf node
    return best_child


def traverse_nodes(node, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    next_node = get_urgent_child(node, state, identity)
    if next_node != None and len(node.untried_actions) == 0 and not state.is_terminal():
        state.apply_move(next_node.parent_action)
        node,state = traverse_nodes(next_node, state, identity)
    else:
        #print ('terminal is %r' % state.is_terminal())
        #if next_node == None:
        #    print('next_node is None')
        #else:
        #    print('next_node is not None')
        #print ('length of untried actions is %i' % len(node.untried_actions))
        return node, state

    return node, state
    # Hint: return leaf_node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    shuffle(node.untried_actions)
    next_action = node.untried_actions.pop()
    state.apply_move(next_action)
    next_node = MCTSNode(parent=node, parent_action=next_action, action_list=state.legal_moves)
    node.child_nodes[next_action] = next_node
    return node.child_nodes[next_action], state
    # Hint: return new_node


def rollout(state, identity):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.

    """
    rollout_state = state.copy()
    # Only play to the specified depth. (estimated max 24 moves possible)
    while rollout_state.is_terminal() == False:
        score_move = None
        for move in rollout_state.legal_moves:
            rollout_test_state = rollout_state.copy()

            rollout_test_score = rollout_test_state.score.get(identity)
            if rollout_test_score == None:
                rollout_test_score = 0

            rollout_test_state.apply_move(move)
            if rollout_test_state.score.get(identity) != None and rollout_test_state.score.get(identity) > rollout_test_score:
                score_move = move
                break

        #Apply scoring move or random move?
        rollout_move = choice(rollout_state.legal_moves)
        if score_move == None:    
            rollout_state.apply_move(rollout_move)
        else:
            rollout_state.apply_move(score_move)

    #Find out if won
    if rollout_state.winner == identity:
        return True
    else:
        return False


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node != None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent


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
        leaf,sampled_game = traverse_nodes(node, sampled_game, identity_of_bot)

        # Expand and roll out unless terminal
        if len(leaf.untried_actions) > 0:
            #Expansion
            new_node,sampled_game = expand_leaf(leaf,sampled_game)
    
            #Rollout
            won = rollout(sampled_game, identity_of_bot)
        else:
            new_node = leaf
            if sampled_game.winner == identity_of_bot:
                won = True
            else:
                won = False
        #Backpropagate
        backpropagate(new_node, won)

    best_action = None
    best_wins = 0
    for action,child in root_node.child_nodes.items():
        if child.wins > best_wins:
            best_wins = child.wins
            best_action = action

    #Prospects are bad...
    if best_action == None:
        best_action = choice(list(root_node.child_nodes.keys()))

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return best_action
