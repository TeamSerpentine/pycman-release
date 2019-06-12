"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

class Compressor(object):
    def __init__(self, input_size):
        """
        Constructor

        Parameters
        ----------
        input_size : [int, int, int]
            size of observations that are put into the compressor

        """

        self.input_size = input_size
        return

    def compress(self, observation):
        """
            Compression function

            Parameters
            ----------
            observation : ndarray with shape equal to self.input_size
                the observation that will be compressed.

            Returns
            -------
            type of ndarray
                compressed_frame
            """
        return

    def decompress(self, observation):
        """
            Decompression function

            Parameters
            ----------
            compressed_frame : ndarray with shape equal to self.output_size
                the observation that will be decompressed.

            Returns
            -------
            type of ndarray
                observation
            """
        return
