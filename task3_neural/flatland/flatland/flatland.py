from enum import IntEnum
import random


class Cell(IntEnum):
    Food = 0
    Poison = 1
    Empty = 2
    Agent = 3


class Orientation(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Turn(IntEnum):
    Left = 0
    Right = 1
    Straight = 2


class Flatland():
    def __init__(self, length, fpd, agent_coord):
        self.grid = [[Cell.Empty for _ in range(length)] for _ in range(length)]

        self.agent_orientation = Orientation.Up
        self.grid[agent_coord[0]][agent_coord[1]] = Cell.Agent

        food_positions = [(x, y) for x in range(length) for y in range(length) if x != y]
        self.food_num = round(fpd[0] * length ** 2)
        for pos in random.sample(food_positions, self.food_num):
            self.grid[pos[0]][pos[1]] = Cell.Food

        poison_positions = [(x, y) for x in range(length) for y in range(length) if
                            x != y and self.grid[x][y] == Cell.Empty]
        self.poison_num = round(fpd[1] * (length ** 2 - self.food_num))
        for pos in random.sample(poison_positions, self.poison_num):
            self.grid[pos[0]][pos[1]] = Cell.Poison

    def __turn(self, turn):
        if turn == Turn.Left:
            self.agent_orientation = Orientation((self.agent_orientation.value - 1) % 4)
        elif turn == Turn.Right:
            self.agent_orientation = Orientation((self.agent_orientation.value + 1) % 4)
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

        return cell_state

    def get_agent(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] == Cell.Agent:
                    return row, col

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
