"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


import glob
from sys import platform
import unittest


def create_test_suite():
    test_file_strings = []
    for depth in ["*", "*/*", "*/*/*"]:
        tests_found = glob.glob(f'{depth}/test_*.py')
        for each in tests_found:
            test_file_strings.append(each)

    module_strings = find_paths(test_file_strings)
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    testSuite = unittest.TestSuite(suites)
    return testSuite


def find_paths(test_file_strings):
    module_strings = []
    # Tested
    if platform == 'win32' or platform == 'cygwin':
        module_strings = [str[:len(str) - 3].replace("\\", ".") for str in test_file_strings]
    if platform == 'linux':
        module_strings = [str[:len(str) - 3].replace("/", ".") for str in test_file_strings]
    if platform == 'darwin':
        module_strings = [str[:len(str) - 3].replace("/", ".") for str in test_file_strings]
    return module_strings


if __name__ == "__main__":
    testSuite = create_test_suite()
    test_runner = unittest.TextTestRunner().run(testSuite)
