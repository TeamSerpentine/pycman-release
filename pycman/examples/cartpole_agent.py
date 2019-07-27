import pycman
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.engine.training import Model
from keras.layers import Dense, Activation
from keras.optimizers import Adam


class CartPoleAgent(pycman.AgentBase):
    def __init__(self, env):
        # variables
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.reward = None
        self.games_played = 0

        # network dimensions
        self.input_shape = env.output_shape[0]
        self.output_shape = env.input_shape[0]

        # construct the network
        self.model = self.construct_network()

    def run(self, env):
        # play 3 games
        for _ in range(20):
            # reset the environment so we are in a new game
            state = env.reset()
            done = False
            while not done:
                action = self.pick_action(state)
                next_state, reward, done, info = env.step(action)
                self.remember(state, action, reward, next_state, done)
                state = next_state
            # increment the amount of games played
            self.games_played += 1

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def pick_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.output_shape)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                         np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def construct_network(self) -> Model:
        model = Sequential()
        model.add(Dense(24, input_dim=self.input_shape, activation="relu"))
        model.add(Dense(24))
        model.add(Dense(2, activation='linear'))
        model.summary()
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model


if __name__ == "__main__":
    # initialize environment
    pycman.env.gym("CartPole-v1")
    # initialize agents
    agents = [CartPoleAgent(pycman.env.get()) for _ in range(1)]
    # add agents
    pycman.agent.add(agents)
    # run pycman
    pycman.run()
