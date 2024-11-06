from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented
import string

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = List[List]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem


class ParkingProblem(Problem[ParkingState, ParkingAction]):
    # A set of points which indicate where a car can be (in other words, every position except walls).
    passages: Set[Point]  # contains (x,y)positions of dots
    # A tuple of points where state[i] is the position of car 'i'.
    cars: Tuple[Point]  # contains (x,y)positions of cars
    # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    # slot[(x,y) , mwgod feh 0 which means slot of park A]=
    slots: Dict[Point, int]
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        temp_point: List[Point]
        initial_state = [['#' for _ in range(self.width)]
                         for _ in range(self.height)]
        for point in self.passages:
            initial_state[point.y][point.x] = '.'
        for point in self.slots.keys():
            initial_state[point.y][point.x] = self.slots[point]
        first_car = 'A'
        for car in self.cars:
            initial_state[car.y][car.x] = first_car
            first_car = chr(ord(first_car)+1)
        return initial_state

    # This function should return True if the given state is a goal. Otherwise, it should return False.

    def is_goal(self, state: ParkingState) -> bool:

        for slot in self.slots.keys():

            if (state[slot.y][slot.x] != chr(self.slots[slot]+65)):
                return False

        return True

    # This function returns a list of all the possible actions that can be applied to the given state

    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        actions = []
        action: ParkingAction
        alphabet_string = string.ascii_uppercase
        alphabet_set = set(alphabet_string)
        for y in range(self.height):
            for x in range(self.width):
                if (state[y][x] in alphabet_set):
                    if (y+1 < self.height and state[y+1][x] not in alphabet_set and state[y+1][x] != '#'):
                        action = ((ord(state[y][x])-65), 'D')
                        actions.append(action)
                    if (y-1 >= 0 and state[y-1][x] not in alphabet_set and state[y-1][x] != '#'):
                        action = ((ord(state[y][x])-65), 'U')
                        actions.append(action)
                    if (x+1 < self.width and state[y][x+1] not in alphabet_set and state[y][x+1] != '#'):

                        action = ((ord(state[y][x])-65), 'R')
                        actions.append(action)

                    if (x-1 >= 0 and state[y][x-1] not in alphabet_set and state[y][x-1] != '#'):
                        action = ((ord(state[y][x])-65), 'L')
                        actions.append(action)
        return actions

    # This function returns a new state which is the result of applying the given action to the given state

    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        point = ()
        car = action[0]
        direction = action[1]
        past_location = (0, 0)
        future_location = (0, 0)
        for y in range(self.height):
            for x in range(self.width):
                if (state[y][x] == chr(car+65)):
                    past_location = Point(x, y)
                    break
        if (direction == Direction.DOWN):
            future_location = Point(past_location.x, past_location.y+1)
        elif (direction == Direction.UP):
            future_location = Point(past_location.x, past_location.y-1)
        elif (direction == Direction.LEFT):
            future_location = Point(past_location.x-1, past_location.y)
        else:  # right
            future_location = Point(past_location.x+1, past_location.y)

        point = Point(past_location.x, past_location.y)
        state[future_location.y][future_location.x] = state[past_location.y][past_location.x]
        keys = self.slots.keys()
        if (point) in keys:
            state[point.y][point.x] = self.slots[point]
        else:
            state[past_location.y][past_location.x] = '.'
        print("outside sucessor:")
        return state

        # This function returns the cost of applying the given action to the given state

    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        car = action[0]
        direction = action[1]
        future_state = []
        past_location = (0, 0)
        for y in range(self.height):
            for x in range(self.width):
                if (state[y][x] == chr(car+65)):
                    past_location = Point(x, y)
                    break
        if (direction == Direction.DOWN):
            future_state = state[past_location.y+1][past_location.x]
        elif (direction == Direction.UP):
            future_state = state[past_location.y-1][past_location.x]
        elif (direction == Direction.LEFT):
            future_state = state[past_location.y][past_location.x-1]
        else:  # right
            future_state = state[past_location.y][past_location.x+1]
        if (future_state == "." or future_state == car):
            return 26-car
        else:
            return 26-car+100

     # Read a parking problem from text containing a grid of tiles

    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip()
                                   for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())


# p = ParkingProblem.from_file('parks/park2.txt')
# initial_state = (p.get_initial_state())
# first_actions = (p.get_actions(initial_state))
# print("initial state is :\n", initial_state)
# print("possible actions from initial state is:\n", first_actions)
# first_successor = p.get_successor(initial_state, (0, 'L'))
# first_cost = p.get_cost(initial_state, (0, 'L'))
# print("first sucessor :\n", first_successor)
# print("first cost:\n", first_cost)
# print("-------------------------------------------------------------------------")
# second_actions = (p.get_actions(first_successor))
# second_successor = p.get_successor(first_successor, (1, 'R'))
# second_cost = p.get_cost(first_successor, (1, 'R'))
# print("possible actions from second state:\n", second_actions)
# print("second sucessor :\n", second_successor)
# print("second cost:\n", second_cost)

# print("-------------------------------------------------------------------------")
# third_actions = (p.get_actions(second_successor))
# third_successor = p.get_successor(second_successor, (1, 'L'))
# third_cost = p.get_cost(first_successor, (1, 'L'))
# print("possible actions from third state:\n", third_actions)
# print("second sucessor :\n", third_successor)
# print("second cost:\n", third_cost)
