import random
import collections


class Direction:
    Left, Right = range(0, 2)


class World():
    def __init__(self, pull_extension=False):
        self.world_width = 30
        self.world_height = 15
        self.simulate_steps = 600
        self.wraparound = True
        self.pull_extension = pull_extension

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

    def pull_object(self):
        new_positions = set()
        object_position_y = list(map(lambda x: x[1], self.object_position))

        for p in object_position_y:
            new_positions.add((self.world_height - 1, p))

        return new_positions


    def simulate(self, ann, move_callback=None, print_stats=False):
        """
        run 600-step simulation and return the fitness
        :param ann ANN
        :param move_callback optional callback called on each tick
        :return fitness of the run
        """

        fitness = 0
        capture_reward = 30
        avoidance_reward = 0
        avoidance_punishment = 40
        partial_punishment = 10

        for i in range(self.simulate_steps):
            self.tick()

            # use ANN to calculate move direction and magnitude
            object_position_y = list(map(lambda x: x[1], self.object_position))
            ann_input = [1 if x in object_position_y else 0 for x in self.tracker_position]

            ann_result = ann.compute(ann_input)
            direction, speed, pull = self.interpret_ann_result(ann_result)
            print(ann_input, ann_result)
            self.move(direction, speed)
            if self.pull_extension and pull:
                self.object_position = self.pull_object()


            if next(iter(self.object_position))[0] == self.world_height:
                self.object_position = self.drop_object()

            # handle the case when object hits the tracker
            if next(iter(self.object_position))[0] == self.world_height - 1:
                shadowing_tracker = [x for x in object_position_y if x in self.tracker_position]

                shadow_size = len(shadowing_tracker)
                object_size = len(self.object_position)
                if shadow_size == object_size:
                #    print("capture")
                    fitness += capture_reward
                elif shadow_size == 0:
                #    print("avoidance", object_position_y, self.tracker_position)
                    if object_size > 4:
                        fitness += avoidance_reward
                    else:
                        fitness -= avoidance_punishment
                # object hit the tracker partially:
                # for small objects count what tracker wasn't able to recover
                # for bigger count what tracker wasn't able to avoid
                else:
                    #print("partial hit")
                    if object_size > 4:
                        fitness -= partial_punishment*shadow_size
                    else:
                        fitness -= partial_punishment*(object_size - shadow_size)

            # check if the callback was set
            if move_callback:
                move_callback(self)

        # normalize fitness to interval [0, 1]
        min_value = (self.simulate_steps / self.world_height) * max(avoidance_punishment, partial_punishment) * -1
        max_value = (self.simulate_steps / self.world_height) * max(avoidance_reward, capture_reward)
        fitness = (fitness - min_value) / (max_value - min_value)

        return fitness

    @staticmethod
    def interpret_ann_result(ann_result):
        # ta sila je ted delana jen podle toho "silnejsiho" neuronu, mozna vzit v uvahu i ten druhej
        #print(ann_result)
        pull_parameter = 0.5
        pull = ann_result[0] + ann_result[1] < pull_parameter
        if ann_result[0] > ann_result[1]:
            return Direction.Left, min([((ann_result[0] - ann_result[1])*5)//1, 4]), pull
        elif ann_result[1] > ann_result[0]:
            return Direction.Right, min([((ann_result[1] - ann_result[0])*5)//1, 4]), pull
        else:
            return Direction.Left, 0, pull