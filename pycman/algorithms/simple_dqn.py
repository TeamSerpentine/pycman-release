"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

# This is necessary for automatic saving and training
from pycman.algorithms.base.algorithm_base import AlgorithmBase

# Algorithm specific imports
import numpy as np
from random import choice
from keras import Sequential
from keras.layers import Dense, Flatten, Conv2D
from keras.optimizers import Adam
from keras.models import model_from_json

# Debugging only
from matplotlib import pyplot


class SimpleDQN(AlgorithmBase):
    """An algorithm that yet has to be implemented."""

    def __init__(self, settings, *args, **kwargs):
        """Constructor. Do not change the super method below!"""
        """Initialize your algorithm here!"""

        print("Extra algorithm arguments:", args)
        print("Extra algorithm keyword arguments:", kwargs)

        # Set all algorithm settings here
        try:
            self.learning_rate = float(kwargs['learning_rate'])
            self.epsilon = float(kwargs['epsilon'])
            self.epsilon_decay = float(kwargs['epsilon_decay'])
        except KeyError:
            raise KeyError("ERROR: Missing a critical constructor parameter for SimpleDQN!")

        # Internal variables
        self.predictions = []

        # Call super
        super().__init__(**settings)

        # Build the model and set it to an internal variable
        self.model = self._build_model()
        return

    def _pick_action(self, observation):
        """
        Chooses an action based on observation during the training phase.

        Parameters
        ----------
        observation: ndarray
            Observation of the current game environment.

        Returns
        -------
        action: int
            Number corresponding to the action that can be taken in the current game state (0 <= \result < n_actions).
        """
        # Add extra dimension to the observation (required for 4D network input)
        observation = np.expand_dims(observation, axis=0)

        # Get the predicted q-values from the network
        pred_q_values = self.model.predict(observation)

        # Save the predicted values for later training
        self.predictions.append(pred_q_values)

        # Check if the agent should act randomly
        if np.random.rand() <= self.epsilon:
            return choice(range(self.action_space))

        # Pick the action based on the predicted reward
        action = np.argmax(pred_q_values[0])

        return action

    def _pick_eval_action(self, observation):
        """
        Chooses an action based on observation for the evaluation phase.

        Parameters
        ----------
        observation: ndarray
            Observation of the current game environment

        Returns
        -------
        action: int
            Number corresponding to the action that can be taken in the current game state (0 <= \result < n_actions)
        """
        # Add extra dimension to the observation (required for 4D network input)
        observation = np.expand_dims(observation, axis=0)

        # Get the predicted q-values from the network
        pred_q_values = self.model.predict(observation)

        # Pick the action based on the predicted reward
        action = np.argmax(pred_q_values[0])

        return action

    def _train(self, observations, metadata):
        """
        This is the implementation of the training which is done after the training condition is met.

        Parameters
        ----------
        observations: list
            All the preprocessed observations in one list
        metadata: panda dataframe
            All the available trainings data, observations, reward, done, info and action taken.

        """

        # Calculate the targets of the network
        # TODO: Calculate q_values and train model

        # Fit the model
        # self.model.fit(observations, target_q_values, batch_size=32, epochs=2, verbose=0)

        # Reset predictions
        self.predictions = []

        # Adjust epsilon
        self.epsilon *= self.epsilon_decay
        return

    def _load_checkpoint(self, path):
        """
        Load an old checkpoint to continue training or retrieving a trained model.

        Parameters
        ----------
        path: string
            A path to the folder from which the checkpoint should be loaded.
        """
        # Load json and create model
        json_file = open(path + "\\model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)

        # Load weights into the restored model
        model.load_weights(path + "\\model.h5")
        print("Loaded model from disk")
        return self._build_model(model=model)

    def _store_checkpoint(self, path):
        """
        Store a checkpoint to later restore or reuse the model.

        Parameters
        ----------
        path: string
            A path to the folder to which the checkpoint should be saved.
        """
        # Save the model to json
        model_json = self.model.to_json()
        with open(path + "\\model.json", "w") as json_file:
            json_file.write(model_json)

        # Serialize weights to HDF5
        self.model.save_weights(path + "\\model.h5")
        return

    """-------------------------------------------------------------------------------------------------------------"""
    """---------------------------------------------Auxiliary functions---------------------------------------------"""
    """-------------------------------------------------------------------------------------------------------------"""

    def _build_model(self, model=None):
        """Builds the model"""

        # If no model is loaded, create a new one
        if model is None:
            model = Sequential()

            # Two convolutional layers
            model.add(Conv2D(4, kernel_size=(8, 8), strides=(6, 6), activation='relu', input_shape=(210, 160, 3)))
            model.add(Conv2D(8, kernel_size=(4, 4), strides=(2, 2), activation='relu'))

            # Flatten everything and add some fully connected/dense layers
            model.add(Flatten())
            model.add(Dense(32, activation='relu'))
            model.add(Dense(self.action_space, activation='linear'))

        # Using the Adam optimizer
        optimizer = Adam(lr=self.learning_rate)

        # Create the model based on the information above
        model.compile(loss='mse',
                      optimizer=optimizer)
        return model
