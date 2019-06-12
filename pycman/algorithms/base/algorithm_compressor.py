"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import zlib
import sys
import numpy
import pandas
import json


class DataIO:
    """ 
    Compresses a string or ndarray and returns you either the string or the json dump of the ndarray
    """
    def __init__(self):
        self.compressor = self._get_data_stream_compressor()
        self.decompressor = self._get_data_stream_decompressor()
        self.encoding_type = "utf-8"

        self._last_obs_for_difference_map = None
        self._difference_map_flag = False

        # TODO calculate differnces for a certain amount of games

    def _restore_observation(self, observation):
        """ Restores the difference map to a full observation. """

        observation = json.loads(observation)
        observation = numpy.array(observation, dtype=numpy.uint8)

        if not getattr(observation, "shape", None):
            return observation

        if observation.shape == (210, 160, 3):
            self._difference_map_flag = True
            self._last_obs_for_difference_map = observation
            return  observation

        if self._difference_map_flag:
            for row in observation:
                self._last_obs_for_difference_map[row[0], row[1], row[2]] = row[3]
            return  self._last_obs_for_difference_map

        return observation

    def _calculate_difference_map(self, observation):
        """
        Makes the whole array smaller by calculating the difference in the map
        Parameters
        ----------
        obs: ndarray
            game observation
        step_id: int
            number of steps in the game
        Returns
        -------
        difference map: ndarray || int
            An array with only the difference and the values that are different with respect to the original.
            Or an integer value of -1, this clears out the observation.
        """

        # Type checking for ndarray
        if type(observation) is not numpy.ndarray:
            return observation

        # Check the correct dimensions
        if observation.shape != (210, 160, 3):
            return observation

        # Was there a previous observation
        if self._last_obs_for_difference_map is None:
            self._last_obs_for_difference_map = observation
            return observation

        # Calculate the difference between the old observation and the new observation
        diff = self._last_obs_for_difference_map - observation

        # Store all the locations of the differences
        indexes = numpy.nonzero(diff)

        # Get a row of the value that changed
        columns_of_indices = numpy.transpose(indexes)
        # Get the value that changed, by using the above indices
        column_of_changed_values = observation[indexes][numpy.newaxis].T
        # create a numpy array, where the last entry is the new value and all but the last one
        # are the indices of the changed value
        new_map_diff = numpy.concatenate([columns_of_indices, column_of_changed_values], axis=1)

        # Change array to list and then to a json dump before encoding it
        return zlib.compress(json.dumps(new_map_diff.tolist()).encode(self.encoding_type), -1)


    def compress(self, compress_data):
        """ Compresses the data if its a string, converts data to string if it is a panda Series or a numpy array """
        if type(compress_data) != str:
            if type(compress_data) == pandas.core.series.Series:
                # Convert every row of the Series, by taking the input and trying to compress it (recursive)
                return compress_data.apply(self._calculate_difference_map)

            elif type(compress_data) == numpy.ndarray:
                compress_data = self._calculate_difference_map(compress_data)
                return zlib.compress(
                        # Change array to list and then to a json dump before encoding it
                        json.dumps(compress_data.tolist()).encode(self.encoding_type), -1)
            else:
                raise ValueError(f"Unable to compress data of type {type(compress_data)} "
                                 f"convert to str or ndarray first")

        return zlib.compress(compress_data.encode(self.encoding_type), -1)

    def decompress(self, decompress_data):
        """  Input is compressed data, output is a json.dump | string.  """
        decompress_data = zlib.decompress(decompress_data).decode(self.encoding_type)
        return self._restore_observation(decompress_data)

    @staticmethod
    def _get_data_stream_compressor():
        """Get the default data compressor object needed to compress data streams."""
        wbits = +15
        return zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, wbits)

    @staticmethod
    def _get_data_stream_decompressor():
        """Get the default data decompressor object needed to decompress data streams."""
        wbits = +15
        return zlib.decompressobj(wbits)

    def _compress_data_stream(self, compress_data):
        """Compress data as a data stream, making appending possible. Takes json strings."""
        return self.compressor.compress(compress_data.encode(self.encoding_type))

    @staticmethod
    def print_msg(msg):
        sys.stdout.write("\r" + msg)
        sys.stdout.flush()