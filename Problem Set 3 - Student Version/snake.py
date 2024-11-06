from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body
    # where the head is the first point and the tail is the last
    direction: Direction    # The direction that the snake is moving towards
    # The location of the apple. If the game was already won, apple will be None
    apple: Optional[Point]


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:

        snake_positions = set(self.snake)
        possible_points = [Point(x, y)
                           for x in range(self.width)
                           for y in range(self.height)
                           if Point(x, y) not in snake_positions
                           ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        if seed is not None:
            # Initialize the random generator using the seed
            self.rng.seed(seed)
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        # The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
        self.snake = list()
        self.snake.append(Point(math.floor(self.width/2),
                          math.floor(self.height/2)))
        self.apple = self.generate_random_apple()
        self.direction = Direction.LEFT
        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def is_opposite(self, Dir1: Direction) -> bool:
        if ((Dir1 == Direction.RIGHT and self.direction == Direction.LEFT) or (self.direction == Direction.RIGHT and Dir1 == Direction.LEFT)):
            return True
        if ((Dir1 == Direction.UP and self.direction == Direction.DOWN) or (self.direction == Direction.UP and Dir1 == Direction.DOWN)):
            return True
        return False

    def Loose(self) -> bool:
        for i in range(len(self.snake)):
            for j in range(i+1, len(self.snake)):
                if (self.snake[i].x == self.snake[j].x and self.snake[i].y == self.snake[j].y):
                    return True
        return False

    def actions(self) -> List[Direction]:

        All_actions = [Direction.LEFT, Direction.RIGHT,
                       Direction.UP, Direction.DOWN, Direction.NONE]
        possible_Actions = []
        for action in All_actions:
            flag = self.is_opposite(action)
            if (action != self.direction and not flag):
                possible_Actions.append(action)
        return possible_Actions

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        new_head, previous_head = self.snake[0], self.snake[0]
        done = False
        reward = 0
        if (action == Direction.NONE):
            action = self.direction
        if (action == Direction.UP):
            if (previous_head.y-1 < 0):  # wrap around
                new_head = Point(previous_head.x, self.height-1)
            else:  # no wrap around
                new_head = Point(previous_head.x, previous_head.y-1)
        elif (action == Direction.DOWN):
            if (previous_head.y+1 == self.height):  # wrap around
                new_head = Point(previous_head.x, 0)
            else:
                new_head = Point(previous_head.x, previous_head.y+1)
        elif (action == Direction.RIGHT):
            if (previous_head.x+1 == self.width):  # wrap around
                new_head = Point(0, previous_head.y)
            else:
                new_head = Point(previous_head.x+1, previous_head.y)
        elif (action == Direction.LEFT):
            if (previous_head.x-1 < 0):  # wrap around
                new_head = Point(self.width-1, previous_head.y)
            else:
                new_head = Point(previous_head.x-1, previous_head.y)

        self.snake.insert(0, new_head)
        if (new_head.x == self.apple.x and new_head.y == self.apple.y):
            self.snake.append(new_head)
            reward += 1
            self.apple = None

        self.snake.pop()
        self.direction = action
        if len(self.snake) == self.width*self.height:
            reward += 100
            done = True
        if (self.Loose()):
            done = True
            reward = -100
        if (not done and self.apple is None):
            self.apple = self.generate_random_apple()
        observation = SnakeObservation(
            tuple(self.snake), self.direction, self.apple)
        return observation, reward, done, {}
    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake),
            self.parse_action(direction),
            Point(*apple)
        )

    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))

    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]

    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]
