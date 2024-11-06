from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented
from math import inf

# This is a class for a generic Value Iteration agent


class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A]  # The MDP used by this agent for training
    utilities: Dict[S, float]  # The computed utilities
    # The key is the string representation of the state and the value is the utility
    discount_factor: float  # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # We initialize all the utilities to be 0
        self.utilities = {state: 0 for state in self.mdp.get_states()}
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        if (self.mdp.is_terminal(state)):
            return 0
        result = -1*inf
        # Given a state and an action, this function returns
        # all possible next states "s'" and their corresponding probabilities P(s'|s, a) as a dictionary
        for action in self.mdp.get_actions(state):
            maximum_utility = 0

            for nextstate, probability in self.mdp.get_successor(state, action).items():
                maximum_utility += probability * \
                    (self.mdp.get_reward(state, action, nextstate) +
                     self.discount_factor*self.utilities[nextstate])
            if (maximum_utility > result):
                result = maximum_utility
        return result

        # TODO: Complete this function
        NotImplemented()

    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    # me: updates the utility of every state based on bellman equation calculated
    def update(self, tolerance: float = 0) -> bool:
        new_utilities = dict()
        for state in self.mdp.get_states():
            bellmanequation_return = self.compute_bellman(state)
            new_utilities.update({state: bellmanequation_return})
        max_change = inf*-1
        for state, utility in new_utilities.items():
            delta = abs(utility-self.utilities[state])
            if (delta > max_change):
                max_change = delta
        self.utilities = new_utilities

        if (max_change > tolerance):
            return False
        else:
            return True

        '''
        QUESTION ::
        ASK DOCTOR YEHYA WHY THIS LOGIC DOESN'T WORK ? 
         def update(self, tolerance: float = 0) -> bool:
        converged = 0
        for state in self.mdp.get_states():
            bellmanequation_return = self.compute_bellman(state)
            if (not (abs(bellmanequation_return-self.utilities[state]) > tolerance)):
                converged += 1
                self.utilities[state] = bellmanequation_return
            else:  # less than or equal tolerance ->converged

                self.utilities[state] = bellmanequation_return
        # all of them converged-minus one for terminal state
        if (converged == len(self.mdp.get_states())):
            return True
        else:
            return False
        
        
        '''

        NotImplemented()

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    # what does this function return ?
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        if (iterations == None):
            return 0
        for i in range(1, iterations+1):
            if (self.update(tolerance) == True):
                # converged
                return i
        return iterations

        # TODO: Complete this function to apply value iteration for the given number of iterations
        NotImplemented()

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:

        if (self.mdp.is_terminal(state)):
            return None
        argmax = None
        Max = inf*-1
        for action in self.mdp.get_actions(state):
            maximum_utility = 0

            for nextstate, probability in self.mdp.get_successor(state, action).items():
                maximum_utility += probability * \
                    (self.mdp.get_reward(state, action, nextstate) +
                     self.discount_factor*self.utilities[nextstate])
            if (maximum_utility > Max):
                Max = maximum_utility
                argmax = action

        return argmax

        NotImplemented()

    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(
                state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(
                state): value for state, value in utilities.items()}
