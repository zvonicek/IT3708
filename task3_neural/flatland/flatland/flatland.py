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

    def simulate(self, ann, move_callback=None, print_stats=False):
        """
        run 60-step simulation and return the fitness
        :param ann ANN
        :param move_callback optional callback called on each tick
        :return fitness of the run
        """

        reward = 0
        food_reward = 1
        poison_punishment = 1

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
            if move_callback:
                move_callback(self)

        # normalize reward to interval [0, 1]
        min_value = self.poison_num * poison_punishment * -1
        max_value = self.food_num * food_reward
        reward = (reward - min_value) / (max_value - min_value)

        if print_stats:
            self.print_stats()

        self.reset()

        return reward

    @staticmethod
    def interpret_result(result, roulette_interpertation=False):
        portions = Flatland.compute_portions(result)
        directions = [Turn.Left, Turn.Straight, Turn.Right]

        if roulette_interpertation:
            rnd = random.uniform(0, 1)

            for d in directions:
                if portions[d][0] <= rnd < portions[d][1]:
                    return d

        # choose the maximum output, if there are more, then randomly
        else:
            max_o = max(result)
            act = []

            for d in directions:
                if result[d] == max_o:
                    act.append(d)

            return random.choice(act)


    @staticmethod
    def compute_portions(sensor_output):
        output_sum = sum(sensor_output)
        prob_sum = 0
        result = {}
        directions = [Turn.Left, Turn.Straight, Turn.Right]

        if output_sum == 0:
            return [(0, 1/3), (1/3, 2/3), (2/3, 1)]

        for o, d in zip(sensor_output, directions):
            new_prob_sum = prob_sum + o/output_sum
            result[d] = (prob_sum, new_prob_sum)
            prob_sum = new_prob_sum

        return result

    def print_stats(self):
        food = 0
        poison = 0

        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] == Cell.Food:
                    food += 1
                elif self.grid[row][col] == Cell.Poison:
                    poison += 1

        print("food eaten:", self.food_num - food, "poison eaten:", self.poison_num - poison)