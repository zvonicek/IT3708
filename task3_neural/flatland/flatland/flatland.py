import random
import collections


class Cell:
    Food, Poison, Empty, Agent = range(0, 4)


class Orientation:
    Up, Right, Down, Left = range(0, 4)


class Turn:
    Left, Right, Straight = range(0, 3)


class Flatland():
    def __init__(self, length, fpd, agent_coord):
        self.grid = [[Cell.Empty for _ in range(length)] for _ in range(length)]

        self.agent_orientation = Orientation.Up
        self.grid[agent_coord[0]][agent_coord[1]] = Cell.Agent
        self.agent_coord = agent_coord

        food_positions = [(x, y) for x in range(length) for y in range(length) if x != y]
        self.food_num = round(fpd[0] * length ** 2)
        for pos in random.sample(food_positions, self.food_num):
            self.grid[pos[0]][pos[1]] = Cell.Food

        poison_positions = [(x, y) for x in range(length) for y in range(length) if
                            x != y and self.grid[x][y] == Cell.Empty]
        self.poison_num = round(fpd[1] * (length ** 2 - self.food_num))
        for pos in random.sample(poison_positions, self.poison_num):
            self.grid[pos[0]][pos[1]] = Cell.Poison

        # copy the grid so as it can be restored for next generation
        self.start_grid = [x[:] for x in self.grid]

    def reset(self):
        """resets the world to initial state"""

        self.agent_orientation = Orientation.Up
        self.grid = [x[:] for x in self.start_grid]

        # find initial agent position
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] == Cell.Agent:
                    self.agent_coord = row, col
                    break

    def __turn(self, turn):
        if turn == Turn.Left:
            self.agent_orientation = (self.agent_orientation - 1) % 4
        elif turn == Turn.Right:
            self.agent_orientation = (self.agent_orientation + 1) % 4
        elif turn == Turn.Straight:
            pass
        else:
            raise Exception("Illegal turn")

    def move(self, turn):
        self.__turn(turn)

        curr_row, curr_col = self.get_agent()
        new_row, new_col = curr_row, curr_col

        if self.agent_orientation == Orientation.Up:
            new_row = (new_row - 1) % len(self.grid)
        elif self.agent_orientation == Orientation.Right:
            new_col = (new_col + 1) % len(self.grid)
        elif self.agent_orientation == Orientation.Down:
            new_row = (new_row + 1) % len(self.grid)
        elif self.agent_orientation == Orientation.Left:
            new_col = (new_col - 1) % len(self.grid)

        cell_state = self.grid[new_row][new_col]

        self.grid[curr_row][curr_col] = Cell.Empty
        self.grid[new_row][new_col] = Cell.Agent
        self.agent_coord = (new_row, new_col)

        return cell_state

    def get_agent(self):
        return self.agent_coord

    def sensor_output(self):
        x, y = self.get_agent()
        l = len(self.grid)
        result = []

        if self.agent_orientation == Orientation.Up:
            surround = [((x - 1) % l, y), (x, (y + 1) % l), ((x + 1) % l, y)]
        elif self.agent_orientation == Orientation.Right:
            surround = [(x, (y + 1) % l), ((x + 1) % l, y), (x, (y - 1) % l)]
        elif self.agent_orientation == Orientation.Down:
            surround = [((x + 1) % l, y), (x, (y - 1) % l), ((x - 1) % l, y)]
        else:
            surround = [(x, (y - 1) % l), ((x - 1) % l, y), (x, (y + 1) % l)]

        for p in surround:
            result.append(self.grid[p[0]][p[1]])

        # result: [Left sensor, Straight sensor, Right sensor]
        return result

    def simulate(self, ann, move_callback=None):
        """
        run 60-step simulation and return the fitness
        :param ann ANN
        :param move_callback optional callback called on each tick
        :return fitness of the run
        """

        reward = 0
        food_reward = 10
        poison_punishment = 5

        # in assignment: 60 time step for moving in flatland
        for i in range(60):
            sensor_output = self.sensor_output()
            food_input = list(map(lambda x: 1 if x == Cell.Food else 0, sensor_output))
            poison_input = list(map(lambda x: 1 if x == Cell.Poison else 0, sensor_output))
            ann_input = food_input + poison_input
            result = ann.compute(ann_input)
            action = self.interpret_result(result)
            eaten = self.move(action)

            if eaten == Cell.Food:
                reward += food_reward
            elif eaten == Cell.Poison:
                reward -= poison_punishment

            # check if the callback was set
            if isinstance(move_callback, collections.Callable):
                move_callback(self)

        # normalize reward to interval [0, 1]
        min_value = self.poison_num * poison_punishment * -1
        max_value = self.food_num * food_reward
        reward = (reward - min_value) / (max_value - min_value)

        self.reset()

        return reward

    @staticmethod
    def interpret_result(result):
        possibilities = []
        if result[0]:
            possibilities.append(Turn.Left)
        if result[1]:
            possibilities.append(Turn.Straight)
        if result[2]:
            possibilities.append(Turn.Right)

        if len(possibilities) == 0:
            possibilities = [Turn.Left, Turn.Straight, Turn.Right]

        return random.choice(possibilities)