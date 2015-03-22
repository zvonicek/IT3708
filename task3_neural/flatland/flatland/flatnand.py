from enum import IntEnum
import random


class Cell(IntEnum):
    Food = 0
    Poison = 1
    Empty = 2
    Agent = 3


class Position(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Flatland():
    def __init__(self, length, fpd):
        self.grid = [[Cell.Empty for _ in range(length)] for _ in range(length)]
        self.position = Position.Up

        food_positions = [(x, y) for x in range(length) for y in range(length) if x != y]
        food_num = round(fpd[0]*length**2)
        for pos in random.sample(food_positions, food_num):
            self.grid[pos[0]][pos[1]] = Cell.Food

        poison_positions = [(x, y) for x in range(length) for y in range(length) if x != y and self.grid[x][y] == Cell.Empty]
        poison_num = round(fpd[1]*(length**2-food_num))
        for pos in random.sample(poison_positions, poison_num):
            self.grid[pos[0]][pos[1]] = Cell.Poison

    def __turn(self, position):
        if position == Position.Left:
            self.position = Position((self.position.value - 1) % 4)
        elif position == Position.Right:
            self.position = Position((self.position.value + 1) % 4)
        elif position == Position.Down:
            raise Exception("Illegal turn")

    def move(self, position):
        self.__turn(position)
        #TODO move
        #TODO check new cell and eat
        pass

    def get_agent(self):
        #TODO
        pass