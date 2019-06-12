"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


import sys
import json
import numpy as np
import unittest
import pandas

from pycman.algorithms.base.algorithm_compressor import DataIO

compressor_check = DataIO


class TestCompressor(unittest.TestCase):

    def setUp(self):
        self.compressor = compressor_check()

        self.size = lambda x: sys.getsizeof(x)
        self.compress = lambda x: self.compressor.compress(x)
        self.decompress = lambda x: self.compressor.decompress(x)

        self.data = np.random.randint(255, size=(210, 160, 3), dtype=np.uint8)

        # Compression for ndarray check
        self.data_ndarray = self.data
        self.compressed_ndarray = self.compress(self.data_ndarray)
        self.decompressed_ndarray = self.decompress(self.compressed_ndarray)
        self.restored_ndarray = self.decompressed_ndarray

        # Compression for json dump check
        self.data_json = json.dumps(self.data.tolist())
        self.compressed_json = self.compress(self.data_json)
        self.decompressed_json = self.decompress(self.compressed_json)
        self.restored_json_ndarray = self.decompressed_json
        self.restored_json = json.dumps(self.restored_json_ndarray.tolist())

    def test_ndarray_equal(self):
        """ Test if we get the same json string back if we enter a ndarray"""
        self.assertEqual(self.restored_json_ndarray.tolist(), self.decompressed_ndarray.tolist(),
                         msg="ndarray is not decompressed properly")

    def test_ndarray_size(self):
        """ Check if the sizes are equal after compression"""
        self.assertEqual(self.size(self.data_ndarray), self.size(self.restored_ndarray),
                         msg="ndarray is not of proper size")

    def test_ndarray_compressing(self):
        size_original = self.size(self.data_json)
        size_compressed = self.size(self.compressed_ndarray)
        self.assertEqual(size_original > size_compressed, True,
                         msg=f"ndarray is not stored smaller than the original (as list) ratio "
                             f"{size_compressed / size_original}")

    def test_ndarray_lossless(self):
        self.assertEqual(np.array_equal(self.data.tolist(), self.restored_ndarray), True,
                         msg="Can not restore original ndarray")

    def test_json_dump(self):
        self.assertEqual(self.data_json, self.restored_json,
                        msg="json_dump is not returned properly")

    def test_json_dump_size(self):
        self.assertEqual(self.size(self.data), self.size(self.decompressed_json),
                         msg="json_dump is not of proper size")

    def test_json_dump_compressing(self):
        size_original = self.size(self.data_json)
        size_compressed = self.size(self.compressed_json)
        self.assertEqual(size_original > size_compressed, True,
                         msg=f"json dump is not stored smaller than the original ratio "
                             f"{size_compressed / size_original}")

    def test_json_dump_lossless(self):

        self.assertEqual(np.array_equal(self.data, self.restored_json_ndarray), True,
                         msg=f"Can not restore original json dump data. (ndarray)")

    def test_ValueError_int(self):
        with self.assertRaises(ValueError):
            self.compressor.compress(5)

    def test_ValueError_list(self):
        with self.assertRaises(ValueError):
            self.compressor.compress([5, 7 , 9])


if __name__ == "__main__":
    unittest.main()