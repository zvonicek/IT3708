from collections import defaultdict
import copy
import random
from reinforcement_flatland.flatland import Flatland, Cell


class QLearning():
    def __init__(self, world_filename, iterations):
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
        # λ
        self.trace_decay = 0.1
        # number of iterations
        self.iter_num = iterations

        self.food_remaining = None
        self.poison_remaining = None
        # q values
        self.q = defaultdict(int)
        # eligibility values
        self.e = defaultdict(int)
        self.eaten = set()
        # frozenset cache (perf)
        self.frozen_eaten = frozenset()
        # best_state cache (perf)
        self.best_action_cache = (None, None)
        # holds an information whether the current run was greedy or exploratory (random)
        self.greedy_run = False
        # cache for the best performing q set
        self.best_cache = None

    def q_learning(self):
        self.q = defaultdict(int)

        for i in range(0, self.iter_num):
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

            if i % 50 == 0:
                print("generation", i)
                self.simulate(None)

        self.simulate(None)

    def move(self, action):
        prev_artifact = self.flatland.move(action)
        if prev_artifact == Cell.Food:
            self.food_remaining -= 1
            self.eaten.add(self.flatland.agent_coord)
            self.frozen_eaten = frozenset(self.eaten)

        return prev_artifact

    def reset(self):
        self.flatland.reset()
        self.food_remaining = self.flatland.food_num
        self.poison_remaining = self.flatland.poison_num
        self.eaten = set()
        self.frozen_eaten = frozenset()
        self.e = defaultdict(int)

    def current_state(self):
        return self.flatland.agent_coord, self.frozen_eaten

    def compute_reward(self, prev_artifact):
        if prev_artifact == Cell.Food:
            return 5
        elif prev_artifact == Cell.Poison:
            return -8
        elif self.flatland.agent_coord == self.flatland.agent_init and self.food_remaining == 0:
            # reward for the finish state
            return 5
        else:
            return 0

    def best_action(self, state):
        if self.best_action_cache[0] == state:
            return self.best_action_cache[1]

        maximum = -float("inf")
        highest = []
        for x in range(4):
            value = self.q[state, x]
            if value > maximum:
                maximum = value
                highest = [x]
            elif value == maximum:
                highest.append(x)

        choice = random.choice(highest)
        self.best_action_cache = (state, choice)

        return choice

    def select_action(self):
        if random.uniform(0, 1) > self.p:
            self.greedy_run = True
            selected_action = self.best_action(self.current_state())
        else:
            self.greedy_run = False
            selected_action = random.choice(range(4))

        return selected_action

    def update_q(self, prev_state, new_state, action, reward):
        q_prev = self.q[prev_state, action]
        q_best_next = self.q[new_state, self.best_action(new_state)]

        self.q[prev_state, action] = q_prev + self.learning_rate * (reward + self.discount_rate*q_best_next - q_prev)

        #self.update_eligibility(prev_state, action, reward, q_best_next, q_prev)

    def update_eligibility(self, prev_state, action, reward, q_best_next, q_prev):
        # on exploratory runs it is recommended to clear the traces
        if not self.greedy_run:
            self.e = defaultdict(int)

        delta = reward + self.discount_rate * q_best_next - q_prev
        self.e[prev_state, action] += 1

        to_delete = []
        for key in self.e:
            val = self.e[key]

            # this prevents increasing _q_ twice for prev_state (it was already set in _update_q_ method)
            if key != (prev_state, action) and reward > 0:
                self.q[key] += self.learning_rate * delta * val
            val *= self.discount_rate * self.trace_decay

            # cleanup (perf)
            if val < 0.01:
                to_delete.append(key)
            else:
                self.e[key] = val

        # cleanup (perf)
        for d in to_delete:
            del self.e[d]

    def simulate(self, move_callback):
        self.reset()
        if move_callback:
            if self.best_cache is not None:
                self.q = self.best_cache[1]

            move_callback(self)

        step_counter = 0
        poison_conter = 0
        while (self.food_remaining > 0 or self.flatland.agent_coord != self.flatland.agent_init) and step_counter < 5000:
            action = self.best_action(self.current_state())
            artifact = self.move(action)
            if artifact == Cell.Poison:
                poison_conter += 1
            step_counter += 1
            if move_callback:
                move_callback(self)

        if poison_conter == 0 and (self.best_cache is None or self.best_cache[0] > step_counter):
            self.best_cache = (step_counter, copy.copy(self.q))

        print("steps:", step_counter, "poisons:", poison_conter)