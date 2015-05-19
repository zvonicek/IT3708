import random
import collections


class Direction:
    Left, Right = range(0, 2)


class World():
    def __init__(self, fitness_params, pull_extension=True, wraparound=True):
        self.world_width = 30
        self.world_height = 15
        self.simulate_steps = 600
        self.wraparound = wraparound
        self.pull_extension = pull_extension
        self.object_pulled = False
        self.object_captured = False
        self.large_object_hit = False
        self.wall_on_right = 0
        self.wall_on_left = 0
        self.wall_hit = False
        self.tracker_position = []
        self.object_position = []
        self.fitness_params = fitness_params
        self.turn_wall_rewards_num = 2

        self.initialize_world()

    def initialize_world(self):
        # initialize tracker
        self.tracker_position = []
        for i in range(5, 10):
            self.tracker_position.append(i)

        self.turn_wall_rewards_num = 2
        # initialize object
        self.object_position = self.generate_object()

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

        # if wraparound is on, use apply modulo on the value; else do not allow moving beyond borders
        if self.wraparound:
            self.tracker_position = list(map(lambda x: func(x) % self.world_width, self.tracker_position))
        else:
            new_tracker_position = list(map(func, self.tracker_position))
            if all(0 <= x < self.world_width for x in new_tracker_position):
                if self.tracker_position[0] == 0 and new_tracker_position[0] != 0:
                    self.wall_hit = True
                elif new_tracker_position[0] == self.world_width - 5 and new_tracker_position[0] != self.world_width - 5:
                    self.wall_hit = True
                self.tracker_position = new_tracker_position
            elif any(x < 0 for x in new_tracker_position):
                self.tracker_position = list(range(5))
            else:
                self.tracker_position = list(range(self.world_width-5, self.world_width))

    def lower_object(self):
        """Simulate one tick and move the object down"""

        new_positions = []
        for row, col in self.object_position:
            new_positions.append((row + 1, col))
        self.object_position = set(new_positions)

    def generate_object(self):
        """Drop new object"""

        length = random.randint(1, 6)
        position = random.randint(0, self.world_width - length)

        positions = set()
        for i in range(length):
            positions.add((0, position + i))

        self.object_pulled = False
        return positions

    def pull_object(self):
        new_positions = []

        for row, col in self.object_position:
            new_positions.append((self.world_height - 1, col))
        self.object_position = set(new_positions)

    def deploy_wall_sensors(self):
        if self.tracker_position[0] == 0:
            self.wall_on_left = 1
        elif self.tracker_position[4] == self.world_width - 1:
            self.wall_on_right = 1
        else:
            self.wall_on_left = 0
            self.wall_on_right = 0

    def compute_tracker_shadowing(self):
        object_position_y = list((map(lambda x: x[1], self.object_position)))
        shadow = [1 if x in object_position_y else 0 for x in self.tracker_position]
        return shadow

    def recompute_fitness(self, fitness):
        shadow_size = len([x for x in self.compute_tracker_shadowing() if x == 1])
        object_size = len(self.object_position)

        if shadow_size == object_size and object_size <= 4:
            fitness += self.fitness_params.capture_reward
            self.object_captured = True
            if self.object_pulled:
                fitness += self.fitness_params.capture_reward
        elif shadow_size == 0 and object_size > 4:
            fitness += self.fitness_params.avoidance_reward
        # object hit the tracker partially:
        elif object_size > 4:
            fitness -= self.fitness_params.capture_punishment
            if self.object_pulled:
                fitness -= self.fitness_params.capture_punishment
            self.large_object_hit = True
        else:
            fitness -= self.fitness_params.avoidance_punishment

        return fitness

    def simulate(self, ann, move_callback=None, turn_wall_reward=20):
        """
        run 600-step simulation and return the fitness
        :param ann ANN
        :param move_callback optional callback called on each tick
        :return fitness of the run
        """

        fitness = 0

        for i in range(self.simulate_steps):
            # check if the callback was set
            if move_callback:
                move_callback(self)

            if self.wall_hit and self.turn_wall_rewards_num:
                self.turn_wall_rewards_num -= 1
                self.wall_hit = False
                fitness += turn_wall_reward
            self.object_captured = False
            self.large_object_hit = False

            # handle the case when object hits the tracker
            is_last_floor = next(iter(self.object_position))[0] == self.world_height - 1
            if is_last_floor:
                fitness = self.recompute_fitness(fitness)
                self.object_position = self.generate_object()

            else:
                self.lower_object()

            # use ANN to calculate move direction and magnitude
            ann_input = self.compute_tracker_shadowing()

            if not self.wraparound:
                self.deploy_wall_sensors()
                ann_input += [self.wall_on_left, self.wall_on_right]
            ann_result = ann.compute(ann_input)
            direction, speed, pull = self.interpret_ann_result(ann_result)
            self.move(direction, speed)

            if pull and not is_last_floor:
                self.pull_object()
                self.object_pulled = True

        # normalize fitness to interval [0, 1]
        min_value = (self.simulate_steps/self.world_height) * max(self.fitness_params.capture_punishment, self.fitness_params.avoidance_punishment) * -1
        max_value = (self.simulate_steps/self.world_height) * max(self.fitness_params.avoidance_reward, self.fitness_params.capture_reward)
        fitness = (fitness - min_value) / (max_value - min_value)

        self.initialize_world()

        return fitness

    def interpret_ann_result(self, ann_result):
        # ta sila je ted delana jen podle toho "silnejsiho" neuronu, mozna vzit v uvahu i ten druhej
        pull = False
        if self.pull_extension:
            pull_parameter = 0.5
            pull = ann_result[2] < pull_parameter
        if ann_result[0] > ann_result[1]:
            return Direction.Left, min([((ann_result[0])*5)//1, 4]), pull
        elif ann_result[1] > ann_result[0]:
            return Direction.Right, min([((ann_result[1])*5)//1, 4]), pull
        else:
            return Direction.Left, 0, pull