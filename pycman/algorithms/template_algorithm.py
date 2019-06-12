"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

# This is necessary for automatic saving and training
from pycman.algorithms.base.algorithm_base import AlgorithmBase

# In case you want to use a preprocessor, make sure that it is imported in the algorithm_base file to work.
from pycman.preprocessors.preprocessor_hackaday import PreProcessor

class TemplateAlgorithm(AlgorithmBase):
    """An algorithm that yet has to be implemented."""

    def __init__(self, settings, *args, **kwargs):
        """Constructor. Do not change the super method below!"""
        super().__init__(**settings)
        """Initialize your algorithm here!"""

        print("Extra arguments:", args)
        print("Extra keyword arguments:", kwargs)
        pass

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
        pass

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
        pass

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
        pass

    def _load_checkpoint(self, path):
        """
        Load an old checkpoint to continue training or retrieving a trained model.

        Parameters
        ----------
        path: string
            A path to the folder from which the checkpoint should be loaded.
        """
        pass

    def _store_checkpoint(self, path):
        """
        Store a checkpoint to later restore or reuse the model.

        Parameters
        ----------
        path: string
            A path to the folder to which the checkpoint should be saved.
        """
        pass
