
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented
from math import inf
from queue import Queue
from typing import Dict, Iterable
from itertools import combinations
# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # corner cases : no solution\
    goals_rows = set()

    goals_cols = set()
    crate_cols = set()
    crate_rows = set()

    crates_row_up = set()
    crates_cols_left = set()
    crates_rows_down = set()
    crates_cols_right = set()

    goal_row_up = set()
    goal_cols_left = set()
    goal_rows_down = set()
    goal_cols_right = set()
    for goal in problem.layout.goals:
        goals_cols.add(goal.x)
        goals_rows.add(goal.y)
        if (goal.x == 1):
            goal_cols_left.add(goal.x)
        if (goal.x == state.layout.width-2):
            goal_cols_right.add(goal.x)
        if (goal.y == 1):
            goal_row_up.add(goal.y)
        if (goal.y == state.layout.height-2):
            goal_rows_down.add(goal.y)

    for crate in state.crates:
        crate_cols.add(crate.x)
        crate_rows.add(crate.y)
        # any crate on the four corners -> gameover:
        if (Point(crate.x, crate.y)not in state.layout.goals and ((Point(crate.x-1, crate.y) not in state.layout.walkable and Point(crate.x, crate.y+1) not in state.layout.walkable) or (Point(crate.x+1, crate.y) not in state.layout.walkable and Point(crate.x, crate.y+1) not in state.layout.walkable) or (Point(crate.x, crate.y-1) not in state.layout.walkable and Point(crate.x-1, crate.y) not in state.layout.walkable) or (Point(crate.x-1, crate.y) not in state.layout.walkable and Point(crate.x, crate.y+1) not in state.layout.walkable))):
            if (crate in problem.layout.goals):
                return 0
            return inf

    for crate in state.crates:
        if (crate.x == 1):  # if two crates are adgajent to each other and adj to a wall , no one of them is on its goal ->game over
            crates_cols_left.add(crate.x)
            if (crate.y+1 in crate_rows and crate.y not in goals_rows and crate.y+1 not in goals_rows):
                return inf
        if (crate.x == state.layout.width-2):
            crates_cols_right.add(crate.x)
            if (crate.y-1 in crate_rows and crate.y not in goals_rows and crate.y-1 not in goals_rows):
                return inf
        if (crate.y == 1):
            if (crate.x+1 in crate_cols and crate.x not in goals_cols and crate.x+1 not in goals_cols):
                return inf
            crates_row_up.add(crate.y)
        if (crate.y == state.layout.height-2):
            if (crate.x-1 in crate_cols and crate.x not in goals_cols and crate.x-1 not in goals_cols):
                return inf
            crates_rows_down.add(crate.y)

    if (len(crates_row_up) > len(goal_row_up) or len(crates_rows_down) > len(goal_rows_down) or len(crates_cols_left) > len(goal_cols_left) or len(crates_cols_right) > len(goal_cols_right)):
        return inf  # if no of goals beside any corner are less than no of crates in this side , gameover

    return weak_heuristic(problem, state)
