import random
import collections


class Direction:
    Left, Right = range(0, 2)


class World():
    def __init__(self):
        self.world_width = 30
        self.world_height = 15
        self.wraparound = True

        # initialize tracker
        self.tracker_position = []
        for i in range(5, 10):
            self.tracker_position.append(i)

        self.object_position = self.drop_object()

    def contains_object(self, row, col):
        if row == self.world_height - 1:
            return False

        return (row, col) in self.object_position

    def contains_tracker(self, row, col):
        if row != self.world_height - 1:
            return False

        return col in self.tracker_position

    def move(self, direction, length):
        """Tracker movement"""

        assert (length <= 4), "Tracker can move at most by 4 steps"

        if direction == Direction.Left:
            func = lambda x: (x - length)
        else:
            func = lambda x: (x + length)
        new_tracker_position = list(map(func, self.tracker_position))

        # if wraparound is on, use apply modulo on the value; else do not allow moving beyond borders
        if self.wraparound:
            self.tracker_position = list(map(lambda x: x % self.world_width, new_tracker_position))
        elif all(0 <= x < self.world_width for x in new_tracker_position):
            self.tracker_position = new_tracker_position

    def tick(self):
        """Simulate one tick and move the object down"""

        new_positions = []
        for row, col in self.object_position:
            new_positions.append((row + 1, col))
        self.object_position = set(new_positions)

    def drop_object(self):
        """Drop new object"""

        length = random.randint(1, 6)
        position = random.randint(0, self.world_width - length)

        positions = set()
        for i in range(length):
            positions.add((0, position + i))

        return positions

    def simulate(self, ann, move_callback=None, print_stats=False):
        """
        run 600-step simulation and return the fitness
        :param ann ANN
        :param move_callback optional callback called on each tick
        :return fitness of the run
        """

        fitness = 0

        for i in range(600):
            self.tick()

            # TODO: use ANN to calculate move direction and magnitude
            self.move(Direction.Right, 4)

            # handle the case when object hits the tracker
            if next(iter(self.object_position))[0] == self.world_height:
                if all(x[1] in self.tracker_position for x in self.object_position):
                    print("capture") # TODO adjust fitness
                elif not any(x[1] in self.tracker_position for x in self.object_position):
                    print("avoidance") # TODO adjust fitness

                self.object_position = self.drop_object()

            # check if the callback was set
            if isinstance(move_callback, collections.Callable):
                move_callback(self)

        return fitness