"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""



import os
import unittest
from pycman.core.gui import start_menu
from pycman.core.gui.auxiliary import os_specific, handler_config


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.test_layout = start_menu.Layout()
        self.handler_config = handler_config.HandlerConfig("player")

    def tearDown(self):
        pass

    def test_image_file_paths(self):
        """Test if os specific file paths exist properly"""
        self.test_layout._os_class = os_specific.Darwin()
        path = self.test_layout._find_path_pictures()
        darwin_paths = os_specific.Darwin.set_logos(path)

        self.test_layout._os_class = os_specific.Linux()
        path = self.test_layout._find_path_pictures()
        linux_paths = os_specific.Linux.set_logos(path)

        self.test_layout._os_class = os_specific.Windows()
        path = self.test_layout._find_path_pictures()
        windows_paths = os_specific.Windows.set_logos(path)

        for file in darwin_paths:
            self.assertTrue(os.path.isfile(file))

        for file in linux_paths:
            self.assertTrue(os.path.isfile(file))

        for file in windows_paths:
            self.assertTrue(os.path.isfile(file))

    def test_handler_config_file_path(self):
        """Test if handler config file path exists"""
        file = self.handler_config._set_default_path()
        self.assertTrue(os.path.isfile(file))
