import enum

import intcode
import repairs


# immutable point http://www.blog.pythonlibrary.org/2014/01/17/how-to-create-immutable-classes-in-python/
class Point:
    def __init__(self, x: int, y: int):
        super(Point, self).__setattr__("x", x)
        super(Point, self).__setattr__("y", y)

    def __str__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __setattr__(self, name, value):
        raise AttributeError("Point is immutable")

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.x == other.x and self.y == other.y

    # returns the direction to move from this point to 'target'
    def direction_to(self, target: 'Point') -> 'Direction':
        if self.x == target.x and self.y < target.y:
            return Direction.DOWN
        elif self.x == target.x and self.y > target.y:
            return Direction.UP
        elif self.x < target.x and self.y == target.y:
            return Direction.RIGHT
        elif self.x > target.x and self.y == target.y:
            return Direction.LEFT
        else:
            raise ValueError(f"Points are not adjacent this={self} target={target}")

    def adjacent_points(self):
        return [self + Direction.DOWN.offset,
                self + Direction.UP.offset,
                self + Direction.LEFT.offset,
                self + Direction.RIGHT.offset]


# https://stackoverflow.com/questions/12680080/python-enums-with-attributes
class Direction(enum.Enum):
    """
    Enumerates directions, their command code on the repair program and the offset
    on an x asis from left to right and y axis from top to bottom
    """
    UP = 1, Point(0, -1)
    DOWN = 2, Point(0, 1)
    LEFT = 3, Point(-1, 0)
    RIGHT = 4, Point(1, 0)

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, offset: (int, int) = None):
        self.offset = offset

    def opposite(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT


class Status(enum.Enum):
    HIT_WALL = 0
    MOVE_SUCCEEDED = 1
    REACHED_OYXGEN_STATION = 2


class MapObject(enum.Enum):
    UNDISCOVERED = ' '
    OPEN = '.'
    WALL = '#'
    OXYGEN = 'O'
    DROID = 'D'
    ORIGIN = 'X'
    PATH = '*'


class Path:
    def __init__(self, initial: list):
        self.steps = initial

    def copy(self):
        return Path(self.steps.copy())

    def pos(self):
        return self.steps[len(self.steps) - 1]

    def append(self, new_pos: Point):
        return self.steps.append(new_pos)

    def backtrack(self):
        return self.steps.pop()

    def print(self):
        print([str(pos) for pos in self.steps])


class PointDirection:
    def __init__(self, pos: Point, direction: Direction):
        self.pos = pos
        self.direction = direction

    def __hash__(self):
        return hash((self.pos, self.direction))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.pos == other.pos and self.direction == other.direction


class Pathfinder:
    def __init__(self):
        self.path = Path([Point(0, 0)])
        self.floor_plan = {Point(0, 0): MapObject.OPEN}
        self.explored_point_directions = set()
        self.explore_order = (Direction.DOWN, Direction.UP, Direction.RIGHT, Direction.LEFT)
        self.repair_robot = None  # init later!
        self.robot_input = []
        self.path_to_oxygen_station = None

    def explore_all_paths_and_find_oxygen_station(self) -> Path:
        iteration = 0
        while True:
            iteration += 1
            direction = self.next_direction_to_explore()
            if direction is None:
                if len(self.path.steps) == 1:  # 1 is origin
                    print(f"Finished: no more steps to backtrack to after {iteration} iterations")
                    break
                self.back_track()
                continue

            self.move_robot_in_direction(direction)

        self.print_floor_plan(iteration)
        return self.path_to_oxygen_station

    def move_robot_in_direction(self, direction):
        next_pos = self.path.pos() + direction.offset
        self.robot_input.append(int(direction.value))
        self.init_robot_if_not_active()
        status = Status(next(self.repair_robot))
        self.explored_point_directions.add(PointDirection(self.path.pos(), direction))
        # print(f"trying from {self.path.pos()} to {direction} is {next_pos}, got status {status}")
        if status == Status.HIT_WALL:
            self.floor_plan[next_pos] = MapObject.WALL
        elif status == Status.MOVE_SUCCEEDED:
            self.path.append(next_pos)
            self.explored_point_directions.add(PointDirection(self.path.pos(), direction.opposite()))
            self.floor_plan[next_pos] = MapObject.OPEN
        elif status == Status.REACHED_OYXGEN_STATION:
            self.path.append(next_pos)
            self.explored_point_directions.add(PointDirection(self.path.pos(), direction.opposite()))
            self.floor_plan[next_pos] = MapObject.OXYGEN
            if self.path_to_oxygen_station is None:
                self.path_to_oxygen_station = self.path.copy()
            print("reached oxygen station")

    def back_track(self):
        dead_end_pos = self.path.backtrack()
        previous_pos = self.path.pos()
        direction_back = dead_end_pos.direction_to(previous_pos)
        self.robot_input.append(int(direction_back.value))
        status = Status(next(self.repair_robot))
        if status != Status.MOVE_SUCCEEDED:
            raise ValueError(f"received status {status} while backtracking from {dead_end_pos} to {previous_pos}")

    def init_robot_if_not_active(self):
        # robot needs an input value directly at start, so create it here once the first input is available
        if self.repair_robot is None:
            program = repairs.program()
            memory = intcode.Memory({i: program[i] for i in range(len(program))})
            self.repair_robot = intcode.run(self.robot_input, memory)

    def next_direction_to_explore(self) -> Direction:
        current_pos = self.path.pos()
        for next_direction in self.explore_order:
            next_try = PointDirection(current_pos, next_direction)
            if next_try in self.explored_point_directions:
                continue
            return next_try.direction

        return None

    def print_floor_plan(self, iteration=None):
        pos_droid = self.path.pos()

        minX = min([pos.x for pos in self.floor_plan.keys()]) - 1
        minY = min([pos.y for pos in self.floor_plan.keys()]) - 1

        maxX = max([pos.x for pos in self.floor_plan.keys()]) + 1
        maxY = max([pos.y for pos in self.floor_plan.keys()]) + 1

        # print(f"iteration {iteration} with grid of width {maxX - minX} and height {maxY - minY}")
        for y in range(minY, maxY, 1):
            for x in range(minX, maxX, 1):
                current_point = Point(x, y)
                symbol = self.floor_plan.get(current_point, MapObject.UNDISCOVERED)
                if current_point in self.path.steps and symbol != MapObject.OXYGEN:
                    if symbol == MapObject.WALL:
                        raise ValueError(f"position {current_point} is a wall but also exists in path")
                    symbol = MapObject.PATH
                if current_point == Point(0, 0):
                    symbol = MapObject.ORIGIN
                elif current_point == pos_droid and symbol != MapObject.OXYGEN:
                    symbol = MapObject.DROID

                print(symbol.value, end="")

            print()
        print()

    def measure_time_for_oxigen_to_fill_locations(self):
        oxygen_positions = self.get_locations(MapObject.OXYGEN)
        open_positions = self.get_locations(MapObject.OPEN)

        iteration = 0
        while len(open_positions) > 0:
            iteration += 1

            adjacent_open_positions = [new_point
                                       for ox in oxygen_positions
                                       for new_point in ox.adjacent_points()
                                       if self.floor_plan[new_point] == MapObject.OPEN]

            for pos in adjacent_open_positions:
                self.floor_plan[pos] = MapObject.OXYGEN

            oxygen_positions = self.get_locations(MapObject.OXYGEN)
            open_positions = self.get_locations(MapObject.OPEN)

        self.print_floor_plan()
        return iteration

    def get_locations(self, position_type: MapObject):
        return [pos for pos, obj in self.floor_plan.items() if obj == position_type]


pathfinder = Pathfinder()
path = pathfinder.explore_all_paths_and_find_oxygen_station()

print(f"part1 = {len(path.steps) - 1}")  # subtract the starting pos

time_for_locations_to_fill = pathfinder.measure_time_for_oxigen_to_fill_locations()
print(f"part 2 = it took {time_for_locations_to_fill} minutes")
