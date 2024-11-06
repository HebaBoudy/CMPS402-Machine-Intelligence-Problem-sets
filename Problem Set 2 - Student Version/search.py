from typing import Tuple, List
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import heapq
import math

# TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)

    terminal, values = game.is_terminal(state)
    if terminal:
        return values[agent], None

    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    ################################ MINIMAX-Desicion ###################################
    (IsTerminal, FinalAns) = game.is_terminal(state)
    if (IsTerminal):
        return (FinalAns[0], None)
    if max_depth == 0:
        return (heuristic(game, state, 0), None)
    ############################# MAX-VALUE #############################################
    if (game.get_turn(state) == 0):  # max node
        MaxSucessorAction = None
        MaxValue = math.inf*-1

        for action in game.get_actions(state):
            MaxSucessorState = game.get_successor(state, action)
            (minimaxReturn, MinResult) = minimax(
                game, MaxSucessorState, heuristic, max_depth-1)
            if (MaxValue < minimaxReturn):
                MaxValue = minimaxReturn
                MaxSucessorAction = action
        return (MaxValue, MaxSucessorAction)
    else:
        ############################## MIN-VALUE ############################################
        # if its min players turns
        MinSucessorAction = None
        MinValue = math.inf
        for action in game.get_actions(state):
            MinSucessorState = game.get_successor(state, action)
            (minimaxReturn, MaxResult) = minimax(
                game, MinSucessorState, heuristic, max_depth-1)
            if (MinValue > minimaxReturn):
                MinValue = minimaxReturn
                MinSucessorAction = action
        return (MinValue, MinSucessorAction)


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return alpha_beta(game, state, heuristic, max_depth, math.inf*-1, math.inf)


def alpha_beta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: int = -1, beta: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    ################################ MINIMAX-Desicion ###################################
    (IsTerminal, FinalAns) = game.is_terminal(state)
    if (IsTerminal):
        return (FinalAns[0], None)
    if max_depth == 0:
        return (heuristic(game, state, 0), None)
    ############################# MAX-VALUE #############################################
    if (game.get_turn(state) == 0):  # max node
        MaxSucessorAction = None
        MaxValue = math.inf*-1

        for action in game.get_actions(state):
            MaxSucessorState = game.get_successor(state, action)
            (minimaxReturn, MinResult) = alpha_beta(
                game, MaxSucessorState, heuristic, max_depth-1, alpha, beta)
            if (MaxValue < minimaxReturn):
                MaxValue = minimaxReturn
                MaxSucessorAction = action
                if (MaxValue >= beta):
                    return (MaxValue, MaxSucessorAction)
                alpha = max(alpha, MaxValue)
        return (MaxValue, MaxSucessorAction)
    else:
        ############################## MIN-VALUE ############################################
        # if its min players turns
        MinSucessorAction = None
        MinValue = math.inf
        for action in game.get_actions(state):
            MinSucessorState = game.get_successor(state, action)
            (minimaxReturn, MaxResult) = alpha_beta(
                game, MinSucessorState, heuristic, max_depth-1, alpha, beta)
            if (MinValue > minimaxReturn):
                MinValue = minimaxReturn
                MinSucessorAction = action
                if (MinValue <= alpha):
                    return (MinValue, MinSucessorAction)
                beta = min(beta, MinValue)
        return (MinValue, MinSucessorAction)


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alpha_beta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: int = -1, beta: int = -1) -> Tuple[float, A]:
    # TODO: Complete this function
    ################################ MINIMAX-Desicion ###################################
    (IsTerminal, FinalAns) = game.is_terminal(state)
    if (IsTerminal):
        return (FinalAns[0], None)
    if max_depth == 0:
        return (heuristic(game, state, 0), None)
    ############################# MAX-VALUE #############################################
    if (game.get_turn(state) == 0):  # max node
        MaxSucessorAction = None
        MaxValue = math.inf*-1
        Max_ordered_actions = []
        heapq.heapify(Max_ordered_actions)
        size = 0

        for action in game.get_actions(state):
            temp = game.get_successor(state, action)
            HeuristicReturn = heuristic(
                game, temp, 0)
            heapq.heappush(Max_ordered_actions,
                           (HeuristicReturn*-1, action, temp))
            size += 1

        for i in range(size):
            action = heapq.heappop(Max_ordered_actions)

            MaxSucessorState = action[2]
            (minimaxReturn, MinResult) = alpha_beta_with_move_ordering(
                game, MaxSucessorState, heuristic, max_depth-1, alpha, beta)
            if (MaxValue < minimaxReturn):
                MaxValue = minimaxReturn
                MaxSucessorAction = action[1]
                if (MaxValue >= beta):
                    return (MaxValue, MaxSucessorAction)
                alpha = max(alpha, MaxValue)
        return (MaxValue, MaxSucessorAction)
    else:
        ############################## MIN-VALUE ############################################
        # if its min players turns
        MinSucessorAction = None
        MinValue = math.inf
        Min_ordered_actions = []
        heapq.heapify(Min_ordered_actions)
        size = 0

        for action in game.get_actions(state):
            temp = game.get_successor(state, action)
            HeuristicReturn = heuristic(
                game, temp, 0)
            heapq.heappush(Min_ordered_actions,
                           (HeuristicReturn, action, temp))
            size += 1

        for i in range(size):
            action = heapq.heappop(Min_ordered_actions)
            MinSucessorState = action[2]
            (minimaxReturn, MaxResult) = alpha_beta_with_move_ordering(
                game, MinSucessorState, heuristic, max_depth-1, alpha, beta)
            if (MinValue > minimaxReturn):
                MinValue = minimaxReturn
                MinSucessorAction = action[1]
                if (MinValue <= alpha):
                    return (MinValue, MinSucessorAction)
                beta = min(beta, MinValue)
        return (MinValue, MinSucessorAction)


def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return alpha_beta_with_move_ordering(game, state, heuristic, max_depth, math.inf*-1, math.inf)
    # TODO: Complete this function
    NotImplemented()

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    ################################ MINIMAX-Desicion ###################################
    (IsTerminal, FinalAns) = game.is_terminal(state)
    if (IsTerminal):
        return (FinalAns[0], None)
    if max_depth == 0:
        return (heuristic(game, state, 0), None)
    ############################# MAX-VALUE #############################################
    if (game.get_turn(state) == 0):  # max node
        MaxSucessorAction = None
        MaxValue = math.inf*-1

        for action in game.get_actions(state):
            MaxSucessorState = game.get_successor(state, action)
            (minimaxReturn, MinResult) = expectimax(
                game, MaxSucessorState, heuristic, max_depth-1)
            if (MaxValue < minimaxReturn):
                MaxValue = minimaxReturn
                MaxSucessorAction = action
        return (MaxValue, MaxSucessorAction)
    else:
        ############################## MIN-VALUE ############################################
        # if its min players turns
        MinSucessorAction = None
        counter = 0
        MinValue = 0

        for action in game.get_actions(state):
            MinSucessorState = game.get_successor(state, action)
            (minimaxReturn, MaxResult) = expectimax(
                game, MinSucessorState, heuristic, max_depth-1)
            # if (MinValue > minimaxReturn):
            #     MinValue = minimaxReturn
            MinSucessorAction = action
            MinValue += minimaxReturn
            counter += 1
        MinValue /= counter

        return (MinValue, MinSucessorAction)
