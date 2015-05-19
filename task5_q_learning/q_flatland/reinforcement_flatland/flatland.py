import random


class Cell:
    Food, Poison, Empty, Agent = range(0, 4)


class Turn:
    Left, Right, Up, Down = range(0, 4)


class Flatland():
    def __init__(self, world, agent_coord, food_num, poison_num):
        self.agent_init = agent_coord
        self.agent_coord = agent_coord
        self.grid = world
        self.food_num = food_num
        self.poison_num = poison_num

        # copy the grid so as it can be restored for next generation
        self.start_grid = [x[:] for x in self.grid]

    @classmethod
    def random_world(cls, length, fpd, agent_coord):
        grid = [[Cell.Empty for _ in range(length)] for _ in range(length)]

        grid[agent_coord[0]][agent_coord[1]] = Cell.Agent

        food_positions = [(x, y) for x in range(length) for y in range(length) if x != y]
        food_num = round(fpd[0] * length ** 2)
        for pos in random.sample(food_positions, food_num):
            grid[pos[0]][pos[1]] = Cell.Food

        poison_positions = [(x, y) for x in range(length) for y in range(length) if
                            x != y and grid[x][y] == Cell.Empty]
        poison_num = round(fpd[1] * (length ** 2 - food_num))
        for pos in random.sample(poison_positions, poison_num):
            grid[pos[0]][pos[1]] = Cell.Poison

        return cls(grid, agent_coord, food_num, poison_num)

    @classmethod
    def from_file(cls, filename):
        grid = []
        food_num = 0
        poison_num = 0
        agent_coord = None

        with open(filename, 'r') as f:
            header = f.readline().split()
            agent_coord = int(header[3]), int(header[2])

            line = f.readline().split()
            while line:
                row = []
                for cell in line:
                    if cell == "-2":
                        row.append(Cell.Agent)
                    elif cell == "-1":
                        row.append(Cell.Poison)
                        poison_num += 1
                    elif cell == "0":
                        row.append(Cell.Empty)
                    else:
                        row.append(Cell.Food)
                        food_num += 1

                grid.append(row)
                line = f.readline().split()

        return cls(grid, agent_coord, food_num, poison_num)

    def reset(self):
        """resets the world to initial state"""

        self.grid = [x[:] for x in self.start_grid]
        self.agent_coord = self.agent_init

    def move(self, turn):
        curr_row, curr_col = self.get_agent()
        new_row, new_col = curr_row, curr_col

        if turn == Turn.Up:
            new_row = (new_row - 1) % len(self.grid)
        elif turn == Turn.Right:
            new_col = (new_col + 1) % len(self.grid[0])
        elif turn == Turn.Down:
            new_row = (new_row + 1) % len(self.grid)
        elif turn == Turn.Left:
            new_col = (new_col - 1) % len(self.grid[0])

        cell_state = self.grid[new_row][new_col]

        self.grid[curr_row][curr_col] = Cell.Empty
        self.grid[new_row][new_col] = Cell.Agent
        self.agent_coord = (new_row, new_col)

        return cell_state

    def get_agent(self):
        return self.agent_coord

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