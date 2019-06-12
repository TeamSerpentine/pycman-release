"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""

import os

from pycman.core.controller.controller import Controller
from pycman.core.gui.auxiliary.handler_config import HandlerConfig

# Here you can set the path to the ini file, which will be loaded
# directly to the controller, without interface
# Please use an absolute path
path = ""

if __name__ == "__main__":

    # In case there is no path set, load default
    if not path:
        path = os.path.join(os.getcwd(), "default_config.ini")

    settings = dict()

    # Load the game settings and the AI settings
    # Please not that the second should always contain at least "AI"
    for each in ["GAME", "AI"]:
        config = HandlerConfig(player_name=each)
        config.load_file(path)

        # Store the GAME and AI settings respectively in the correct format
        settings[each] = config.create_export_code()

    Controller(**settings["GAME"], players=dict(AI=settings["AI"]))
