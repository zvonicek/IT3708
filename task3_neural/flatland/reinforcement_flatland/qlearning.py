import random
from reinforcement_flatland.flatland import Flatland, Cell


class QLearning():
    def __init__(self, world_filename):
        if world_filename is None:
            self.flatland = Flatland.random_world(40, (1/3, 1/3), (2, 3))
        else:
            self.flatland = Flatland.from_file(world_filename)

        # probability of choosing random action
        self.p = 0.2

        # α
        self.learning_rate = 0.2
        # γ
        self.discount_rate = 0.9

        self.food_remaining = None
        self.poison_remaining = None
        self.q = {}
        self.eaten = set()

    def q_learning(self):
        self.q = {}

        for i in range(0, 99):
            self.reset()
            while self.food_remaining > 0 or self.flatland.agent_coord != self.flatland.agent_init:
                prev_state = self.current_state()

                # select action to do
                action = self.select_action()

                # update game
                prev_artifact = self.move(action)

                new_state = self.current_state()
                reward = self.compute_reward(prev_artifact)

                # update array
                self.update_q(prev_state, new_state, action, reward)

        print(self.q)

    def move(self, action):
        prev_artifact = self.flatland.move(action)
        if prev_artifact == Cell.Food:
            self.food_remaining -= 1
            self.eaten.add(self.flatland.agent_coord)

        return prev_artifact

    def reset(self):
        self.flatland.reset()
        self.food_remaining = self.flatland.food_num
        self.poison_remaining = self.flatland.poison_num
        self.eaten = set()

    def current_state(self):
        return self.flatland.agent_coord, frozenset(self.eaten)

    def compute_reward(self, prev_artifact):
        if prev_artifact == Cell.Food:
            return 1
        elif prev_artifact == Cell.Poison:
            return -5
        else:
            return 0

    def best_action(self, state):
        return max(list(range(4)), key=lambda x: self.q.get((state, x), 0))

    def select_action(self):
        if random.uniform(0, 1) > self.p:
            selected_action = self.best_action(self.current_state())
        else:
            selected_action = random.choice(range(4))

        return selected_action

    def update_q(self, prev_state, new_state, action, reward):
        q_prev = self.q.get((prev_state, action), 0)
        q_max_next = self.q.get(new_state, self.best_action(new_state))

        self.q[prev_state, action] = q_prev + self.learning_rate * (reward + self.discount_rate*q_max_next - q_prev)

    def simulate(self, move_callback):
        self.reset()
        while self.food_remaining > 0 or self.flatland.agent_coord != self.flatland.agent_init:
            action = self.best_action(self.current_state())
            self.move(action)
            if move_callback:
                move_callback(self.flatland)