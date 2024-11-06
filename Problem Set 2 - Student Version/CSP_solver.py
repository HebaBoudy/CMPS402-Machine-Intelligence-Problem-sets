from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
from math import inf
import heapq


# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.


def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {
            value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic,
#       we order them in the same order in which they appear in "problem.variables".


def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(
        problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.
# 3/3


def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    binary_constrain: BinaryConstraint
    other_variable: str
    for constrain in problem.constraints:
        if (type(constrain) == BinaryConstraint):
            binary_constrain = constrain
            if (assigned_variable in binary_constrain.variables):
                other_variable = binary_constrain.get_other(assigned_variable)
                if (other_variable not in domains.keys()):
                    continue  # already assigned
                # couldn't remove elements from the domain directly ->Runtime error : change in size of loop
                new_domain = set()
                for value in domains[other_variable]:
                    if (binary_constrain.is_satisfied({assigned_variable: assigned_value, other_variable: value})):
                        new_domain.add(value)
                domains[other_variable] = new_domain
                if (len(domains[other_variable]) == 0):
                    return False
    return True
# This function is used in Least constraining values to sort a list of tuples [(remaining elements in neighbours domains , variable)]
# according to the largest remaining values , if equal then compare by the second entry which is the variable (low to high)


def sort_tuples(lst):
    sorted_lst = sorted(lst, key=lambda x: (-x[0], x[1]))
    return sorted_lst
# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic,
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.


def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    final_ans_tuple = []
    final_ans_list = []
    binary_constrain: BinaryConstraint
    other_variable: str
    # tuple containing(value, no of elements left in the neighbouring variables) structured as PQ to sort them
    for value_outer_loop in domains[variable_to_assign]:
        # total number of elements left in neighbouring domains due to outerloop value assingment
        total_adj_elements_domains = 0
        for constrain in problem.constraints:
            counter = 0
            if (type(constrain) == BinaryConstraint):
                binary_constrain = constrain
                other_variable = binary_constrain.get_other(
                    variable_to_assign)
                if (other_variable not in domains.keys()):
                    continue  # already assigned
                for value_inner_loop in domains[other_variable]:
                    if (binary_constrain.is_satisfied({variable_to_assign: value_outer_loop, other_variable: value_inner_loop})):
                        counter += 1
                total_adj_elements_domains += counter

        final_ans_tuple.append((total_adj_elements_domains, value_outer_loop))

    final_ans_tuple = sort_tuples(final_ans_tuple)
    for i in range(len(final_ans_tuple)):
        final_ans_list.append(final_ans_tuple[i][1])
    return final_ans_list


def solve(problem: Problem) -> Optional[Assignment]:

    assignments = {}
    domains_copy = problem.domains  # Don't change in  problem.domains
    return Back_Tracking(problem, assignments, domains_copy)


def Back_Tracking(problem: Problem, assignments: Assignment, domains: Dict[str, set]) -> Optional[Assignment]:
    if (not one_consistency(problem)):
        return None
    if (problem.is_complete(assignments)):  # must be called once ->autograder
        return assignments
    variable = minimum_remaining_values(problem, domains)
    values = least_restraining_values(problem, variable, domains)
    for value in values:
        domain_copy = domains.copy()
        # The variable to be assigned should be removed from unassinged values (should not taken into considerations of other variables when assinging them  )
        domain_copy.pop(variable)
        forward_checking_valid = forward_checking(
            problem, variable, value, domain_copy)
        if (forward_checking_valid):
            assignments.update({variable: value})
            if (Back_Tracking(
                    problem, assignments, domain_copy)):
                return assignments
             # remove variable from assigned if it violates any neighbouring constraints and try another value "backtracking"
            assignments.pop(variable)
    return None
