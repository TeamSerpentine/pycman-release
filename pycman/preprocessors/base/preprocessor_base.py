"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""
from abc import ABC
from abc import abstractmethod


class PreProcessorBase(ABC):

    def __init__(self):
        """Preprocessor Constructor"""
        return

    @abstractmethod
    def preprocess(self, observation):
        """
        This will convert the actual observation to the preprocessed one.

        Parameters
        ----------
        observation: ndarray
            An ndarray containing the observation for this environment.

        Returns
        -------
        any: any
            Its type and name are up to user specification.
        """
        pass

    @abstractmethod
    def get_output_size(self):
        """
        This function can be used in your network as the proper input size.

        Returns
        -------
        any: any
            A description of the preprocessed item, likely ndarray dimensions.

        """
        pass
