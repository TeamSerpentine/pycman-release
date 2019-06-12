"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""
from pycman.preprocessors.base.preprocessor_base import PreProcessorBase


class PreProcessor(PreProcessorBase):

    def __init__(self, *args, **kwargs):
        super().__init__()
        """ You can give the preprocessor any input arguments.  """

        print("Extra arguments:", *args)
        print("Extra keyword arguments:", kwargs)

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
        return observation

    def get_output_size(self):
        """
        This function can be used in your network as the proper input size.

        Returns
        -------
        any: any
            A description of the preprocessed item, likely ndarray dimensions.

        """
        return (210, 160, 3)
