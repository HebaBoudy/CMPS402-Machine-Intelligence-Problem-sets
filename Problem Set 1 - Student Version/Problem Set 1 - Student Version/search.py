from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import heapq
from typing import List

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    node: S  # the current state
    child: S  # successor of the current state
    parents = dict()  # saving parents for every node#saving parents for every node
    Q: deque[S] = deque()
    explored: set[S] = set()  # for graph implementation
    path = []  # final answer
    if (problem.is_goal(initial_state)):
        return path
    Q.append(initial_state)  # push the root to the fronteir
    while (len(Q) != 0):  # do untill the fronteir is empty
        node = Q.popleft()  # FIFO
        explored.add(node)  # mark as explored
        for action in problem.get_actions(node):  # get all actions
            child = problem.get_successor(node, action)
            if (child not in explored and child not in Q):
                if problem.is_goal(child):
                    # the last element in the path is the goal itself
                    # path.appendleft(action)
                    parents.update({child: (node, action)})
                    # backtrack parents until we reach the initial_state
                    while (1):
                        # add every parent to the begening of the path
                        path.insert(0, parents[child][1])
                        # set the child to its parent to repeat
                        child = parents[child][0]
                        if (child == initial_state):
                            break
                    return path
                else:  # not goal -> enqueue and set save its parent
                    Q.append(child)  # add to the fronteir

                    parents.update({child: (node, action)})
    return None  # reaching this line means no goal found


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    node: S  # the current state
    child: S  # successor of the current state
    parents = dict()  # saving parents for every node
    Q: deque[S] = deque()     # Stack
    explored: set[S] = set()  # for graph implementation
    path: deque[S] = deque()  # final answer
    if (problem.is_goal(initial_state)):  # trivial case
        return path
    Q.append(initial_state)  # push the root to the fronteir
    while (len(Q) != 0):   # do untill the fronteir is empty
        node = Q.pop()  # expand the first node in the stack
        explored.add(node)  # mark as explored
        if (problem.is_goal(node)):
            while (node != initial_state):  # loop until the parent is the initial state
                # add the action that lad to this child to the path from left to be in reverse order
                # parents[node][0] is the state of parent while parents [node][1] is the action
                path.appendleft(parents[node][1])
                # set the child to be its parent and backtrack
                node = parents[node][0]
            return path
        # else
        for action in problem.get_actions(node):  # get all actions
            child = problem.get_successor(node, action)
            if (child not in explored and child not in Q):
                Q.append(child)  # add to the fronteir
                # save its parent and the state
                parents.update({child: (node, action)})
    return None  # reaching this line means no goal found


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    order = 0
    node_tuple = ()   # the current state
    child_tuple = ()  # successor of the current state
    parents = dict()  # saving parents for every node
    # each element in the PQ is tuple of (cost,order,state )
    Q = [(0, 0, initial_state)]
    heapq.heapify(Q)  # initialize list Q as PQ
    explored = set()  # let initial state initially explored
    path: deque[S] = deque()    # final answer list
    if problem.is_goal(initial_state):
        return path  # retun empty :initial state is excluded in testcases

    while len(Q) != 0:  # do untill the fronteir is empty
        node_tuple = heapq.heappop(Q)  # pop the parent node
     #   node_tuple[3] contains action , node_tuple[2] contains the curr state ,node_tuple[1] contains the order, node_tuple[0] contains cost
        if problem.is_goal(node_tuple[2]):

            while (node_tuple[2] != initial_state):
                path.appendleft(node_tuple[3])
                node_tuple = parents[node_tuple]
            return path
        if node_tuple[2] not in explored:
            explored.add(node_tuple[2])
        # else if the state is not the goal:
            # get all actions
            for action in problem.get_actions(node_tuple[2]):
                child_cost = problem.get_cost(node_tuple[2], action)
                child_state = problem.get_successor(node_tuple[2], action)
                if (child_state not in explored):
                    order += 1
                    child_tuple = (
                        child_cost+node_tuple[0], order, child_state, action)
                    # if two costs are equal , order will resolve it
                    heapq.heappush(Q, child_tuple)
                    parents.update({child_tuple: node_tuple})

    return None


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    order = 0
    node_tuple = ()   # the current state
    child_tuple = ()  # successor of the current state
    parents = dict()  # saving parents for every node
    # each element in the PQ is tuple of (cost,order,state )
    Q = [(0, 0, initial_state)]
    Q_states = set()  # search for states in the fronteir in O(1) instead of searching in Q
    Q_states.add(initial_state)
    heapq.heapify(Q)  # initialize list Q as PQ
    explored = set()  # let initial state initially explored
    path: deque[S] = deque()    # final answer list
    if problem.is_goal(initial_state):
        return path  # retun empty :initial state is excluded in testcases

    while len(Q) != 0:  # do untill the fronteir is empty
        node_tuple = heapq.heappop(Q)  # pop the parent node
        Q_states.remove(node_tuple[2])
        explored.add(node_tuple[2])
     #   node_tuple[3] contains action , node_tuple[2] contains the curr state ,node_tuple[1] contains the order, node_tuple[0] contains cost
        if problem.is_goal(node_tuple[2]):
            while (node_tuple[2] != initial_state):
                path.appendleft(node_tuple[3])
                node_tuple = parents[node_tuple]
            return path
       # else if the state is not the goal:
        for action in problem.get_actions(node_tuple[2]):  # get all actions
            child_cost = problem.get_cost(node_tuple[2], action)
            child_state = problem.get_successor(node_tuple[2], action)
            if (child_state not in explored and child_state not in Q_states):
                order += 1
                child_tuple = (
                    child_cost+node_tuple[0]+heuristic(problem, child_state)-heuristic(problem, node_tuple[2]), order, child_state, action)
                # if two costs are equal , order will resolve it
                heapq.heappush(Q, child_tuple)
                Q_states.add(child_state)
                # set its parent in the parents dict
                parents.update({child_tuple: node_tuple})

    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    order = 0
    node_tuple = ()   # the current state
    child_tuple = ()  # successor of the current state
    parents = dict()  # saving parents for every node
    # each element in the PQ is tuple of (cost,order,state )
    Q = [(heuristic(problem, initial_state), 0, initial_state)]
    Q_states = set()  # search for states in the fronteir in O(1) instead of searching in Q
    Q_states.add(initial_state)
    heapq.heapify(Q)  # initialize list Q as PQ
    explored = set()  # let initial state initially explored
    path: deque[S] = deque()    # final answer list
    if problem.is_goal(initial_state):
        return path  # retun empty :initial state is excluded in testcases

    while len(Q) != 0:  # do untill the fronteir is empty
        node_tuple = heapq.heappop(Q)  # pop the parent node
        Q_states.remove(node_tuple[2])
        explored.add(node_tuple[2])
     #   node_tuple[3] contains action , node_tuple[2] contains the curr state ,node_tuple[1] contains the order, node_tuple[0] contains cost
        if problem.is_goal(node_tuple[2]):
            while (node_tuple[2] != initial_state):
                path.appendleft(node_tuple[3])
                node_tuple = parents[node_tuple]
            return path
       # else if the state is not the goal:
        for action in problem.get_actions(node_tuple[2]):  # get all actions
            child_cost = problem.get_cost(node_tuple[2], action)
            child_state = problem.get_successor(node_tuple[2], action)
            if (child_state not in explored and child_state not in Q_states):
                order += 1
                child_tuple = (
                    heuristic(problem, child_state), order, child_state, action)
                # if two heuristics are equal , order will resolve it
                heapq.heappush(Q, child_tuple)
                Q_states.add(child_state)
                # set its parent in the parents dict
                parents.update({child_tuple: node_tuple})
    return None
