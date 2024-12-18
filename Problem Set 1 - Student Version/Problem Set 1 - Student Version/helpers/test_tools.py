from typing import List, Optional, Set, Tuple
from agents import HeuristicFunction
from graph import GraphRoutingProblem, graphrouting_heuristic
from sokoban import SokobanProblem, Direction
from problem import A, S, Problem
from .utils import Result, fetch_recorded_calls, fetch_tracked_call_count, load_function
from .heuristic_checks import InconsistentHeuristicException, test_heuristic_consistency
from functools import lru_cache
import time


def run_parking_trajectory(
        problem: Problem[S, A],
        path: List[A]) -> Tuple[Problem[S, A], List[A], S, float]:
    state = problem.get_initial_state()
    total_cost = 0
    for car, direction in path:
        action = (car, Direction(direction))
        total_cost += problem.get_cost(state, action)
        state = problem.get_successor(state, action)
    return problem, path, state, total_cost


def check_parking_problem(
    output: Tuple[Problem[S, A], List[A], S, float],
    path_cost: float,
    is_goal: bool,
    actions: Optional[Set[A]],
    level_path: str
) -> Result:
    problem, path, state, total_cost = output
    message = "Level:\n"
    message += open(level_path, 'r').read()
    message += "\n"
    message += f"Path: {path}"
    message += "\n"
    if total_cost != path_cost:  # change me
        return Result(False, 0, message + f"Path Cost - Expected: {path_cost}, Got: {total_cost}")
    is_goal_result = problem.is_goal(state)
    if is_goal_result != is_goal:
        return Result(False, 0, message + f"Is the last state a goal? - Expected: {is_goal}, Got: {is_goal_result}")
    if actions is not None:
        actions_result = {(car, str(direction))
                          for car, direction in problem.get_actions(state)}
        if actions_result != actions:
            return Result(False, 0, message + "The possible actions from the last state:\n" + f"Expected: {actions}" + "\n" + f"Got: {actions_result}")
    return Result(True, 1, "")


def run_uninformed_search_for_graph_routing(
        function_path: str,
        problem: GraphRoutingProblem) -> Tuple[List[str], List[str]]:
    fetch_recorded_calls(GraphRoutingProblem.get_actions)
    search_fn = load_function(function_path)
    initial_state = problem.get_initial_state()
    path = search_fn(problem, initial_state)
    traversal = [call["args"][1]
                 for call in fetch_recorded_calls(GraphRoutingProblem.get_actions)]
    return (None if path is None else [node.name for node in path]), [node.name for node in traversal]


def run_informed_search_for_graph_routing(
        function_path: str,
        problem: GraphRoutingProblem) -> Tuple[List[str], List[str]]:
    fetch_recorded_calls(GraphRoutingProblem.get_actions)
    search_fn = load_function(function_path)
    initial_state = problem.get_initial_state()
    path = search_fn(problem, initial_state, graphrouting_heuristic)
    traversal = [call["args"][1]
                 for call in fetch_recorded_calls(GraphRoutingProblem.get_actions)]
    return (None if path is None else [node.name for node in path]), [node.name for node in traversal]


def compare_search_results_for_graph_routing(
        output: Tuple[List[str], List[str]],
        possible_outputs: List[Tuple[List[str], List[str]]],
        fig_path: str) -> Result:
    path, traversal = output
    for expected_path, expected_traversal in possible_outputs:
        if path == expected_path and traversal == expected_traversal:
            return Result(True, 1, "")
    nl = '\n'

    def list_to_str(l): return "No solution" if l is None else repr(
        l)  # '->'.join(l)

    def out_to_str(
        o): return f'- Path: {list_to_str(o[0])} (Excluding the initial state){nl}- Expansion Order: {list_to_str(o[1])}'
    expected = '\nor\n'.join(out_to_str(expected)
                             for expected in possible_outputs)
    fig = open(fig_path, 'r').read()
    message = f"Graph:{nl}{fig}{nl}Expected:{nl}{expected}{nl}Got:{nl}{out_to_str(output)}"
    return Result(False, 0, message)


def run_uninformed_search_for_sokoban(
        function_path: str,
        problem: SokobanProblem()) -> Tuple[str, int]:
    fetch_tracked_call_count(SokobanProblem.get_actions)
    search_fn = load_function(function_path)
    initial_state = problem.get_initial_state()
    path = search_fn(problem, initial_state)
    explored = fetch_tracked_call_count(SokobanProblem.get_actions)
    return (None if path is None else ''.join(str(action) for action in path)), explored


def run_informed_search_for_sokoban(
        function_path: str,
        problem: SokobanProblem,
        heuristic: HeuristicFunction) -> Tuple[str, int]:
    fetch_tracked_call_count(SokobanProblem.get_actions)
    search_fn = load_function(function_path)
    initial_state = problem.get_initial_state()
    path = search_fn(problem, initial_state, heuristic)
    explored = fetch_tracked_call_count(SokobanProblem.get_actions)
    return (None if path is None else ''.join(str(action) for action in path)), explored


def compare_search_results_for_sokoban(
        output: Tuple[str, int],
        possible_outputs: List[Tuple[str, int]],
        level_path: str) -> Result:
    nl = '\n'

    def path_to_str(
        l): return "No solution" if l is None else f'{l} (length={len(l)} steps)'
    for expected_output in possible_outputs:
        if output == expected_output:
            return Result(True, 1, f"Path: {path_to_str(output[0])} - Expanded {output[1]} nodes")
    expected = '\nor\n'.join(
        f'- Path: {path_to_str(path)}{nl}- Expanded {explored} nodes' for path, explored in possible_outputs)
    level = open(level_path, 'r').read()
    message = f"Level:{nl}{level}{nl}Expected:{nl}{expected}{nl}Got:{nl}- Path: {path_to_str(output[0])}{nl}- Expanded {output[1]} nodes"
    return Result(False, 0, message)


def test_sokoban_heuristic(
        function_path: str,
        problem: SokobanProblem) -> Tuple[float, int, str, float]:
    fetch_tracked_call_count(SokobanProblem.get_actions)
    heuristic = lru_cache(
        2**16)(load_function("sokoban_heuristic.strong_heuristic"))
    original_get_successor = SokobanProblem.get_successor
    SokobanProblem.get_successor = test_heuristic_consistency(
        heuristic)(SokobanProblem.get_successor)
    search_fn = load_function(function_path)
    initial_state = problem.get_initial_state()
    message = ""
    start = time.time()
    try:
        path = search_fn(problem, initial_state, heuristic)
    except InconsistentHeuristicException as err:
        message = "Heuristic is inconsistent:\n" + str(err)
        return None, 1e10, message, 0
    finally:
        SokobanProblem.get_successor = original_get_successor
    elapsed = time.time() - start
    explored = fetch_tracked_call_count(SokobanProblem.get_actions)
    path_cost = None
    if path is not None:
        path_cost = 0
        state = initial_state
        for action in path:
            path_cost += problem.get_cost(state, action)
            state = problem.get_successor(state, action)
        goal_h = heuristic(problem, state)
        if goal_h != 0:
            message = f"Expected Heuristic at goal to be 0, got {goal_h}" + "\nGoal State:\n" + str(
                state)
    return path_cost, explored, message, elapsed


def compare_heuristic_for_sokoban(
        output: Tuple[int, str, float],
        expected_path_cost: float,
        thresholds: List[int],
        level_path: str) -> Result:
    path_cost, explored, message, elapsed = output
    if message:
        return Result(False, 0, message)
    if path_cost != expected_path_cost:
        return Result(False, 0, f"Expected path cost to be {expected_path_cost}, got {path_cost}."
                      + "\nEither the A* search implementation is wrong or the heuristic is inconsistent.")
    grade = sum(threshold >= explored for threshold in thresholds)
    message = f"Expanded {explored} nodes in {elapsed} seconds"
    if grade != len(thresholds):
        message += '\n' + f'grade = 0 if nodes > {thresholds[0]}'
        for i, (u, l) in enumerate(zip(thresholds[:-1], thresholds[1:])):
            message += '\n' + f'grade = {i+1} if {u} >= nodes > {l}'
        message += '\n' + \
            f'grade = {len(thresholds)} if {thresholds[-1]} >= nodes'
    return Result(grade != 0, grade, message)
