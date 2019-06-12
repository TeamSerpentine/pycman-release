"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


GUI_NAME = "Pycman gui - Version 0.8 Alpha"


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_SIZE = f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"

# Specifies the column width of all things that have to be centered.
# This is also related to the maximum number of players.
CENTERED = 5

PADDING = [20, 20]
INPADDING = [40, 40]

STRING = 0
BOOLEAN = 1
INT = 2
FIXED = 5

EMPTY_SECTION = "EMPTY"

SPECIAL_TYPES = dict(session_restore=BOOLEAN,
                     boost=BOOLEAN,
                     render=BOOLEAN,
                     can_train=BOOLEAN,
                     store_data=BOOLEAN,
                     store_video=BOOLEAN,
                     fps=INT,

                     # FIX Compressor in gui
                     compressor=FIXED,

                     # Human settings, don't need to be change
                     keys=FIXED,
                     player=FIXED,
                     save_highscores=BOOLEAN)

# To handle empty sections in AI
SPECIAL_TYPES[EMPTY_SECTION] = FIXED

BUTTONS_BOOLEAN = ["True", "False"]
BUTTONS_HOME_MENU = ["LOAD AI", "SAVE", "RESET", "ADD HUMAN", "ADD AI"]
BUTTONS_PLAYER = ["DELETE PLAYER", "GAME SETTINGS", "RUN GAME", "SWITCH/SHOW PLAYER", "ADD PARAMETER"]
BUTTONS_RUNNING_GAME = ["PAUSE GAME", "TERMINATE GAME AND GUI"]

MENU_FILE = ["Open", "Save", "-", "Show help", "Disable help", "Close"]

# MsPacman ['NOOP', 'UP', 'RIGHT', 'LEFT', 'DOWN', 'UPRIGHT', 'UPLEFT', 'DOWNRIGHT', 'DOWNLEFT']
KEYS_HUMAN_1 = ["0", "<Up>", "<Right>", "<Left>", "<Down>"]
KEYS_HUMAN_2 = ["0", "w", "d", "a", "s"]

LIMIT_PLAYER_HUMAN = 2
LIMIT_PLAYER_AI = 16
LIMIT_PLAYER_TOTAL = 16
LIMIT_PLAYER_PER_ROW = 4

PLAYER_HUMAN = "HUMAN"
PLAYER_AI = "AI"
PLAYER_GAME = "GAME"

TOOLTIPS = {
    # Add the help for the Game controls
    f"{PLAYER_GAME};compressor": "If you want to store data, this will compress the frames, can be left empty",
    f"{PLAYER_GAME};fps": "Number of frames shown when rendering the game, 0 is as fast as possible",
    f"{PLAYER_GAME};game_name": "Name of the Atari Game, this need to include version as well (e.g. Breakout-v0)",
    f"{PLAYER_GAME};render": "If True will render the game either to the gui or using the Atari render function",
    f"{PLAYER_GAME};save_folder": "Path where you want to store data, you can use the place holder 'game_name', "                    
                                  "for the actual game name, and it will automatically append the session name.",
    f"{PLAYER_GAME};session_name": "Can be used to distinguish between users, or different settings",
    f"{PLAYER_GAME};session_restore": "If True it will try to continue training from the last point onwards",
    f"{PLAYER_GAME};store_data": "If True it will store the data to the disk at the location specified in save folder",

    # Add the help to AI players
    "Algorithm;algorithm_name": "The name of the algorithm_base, it does have to be imported in the controller in order "
                                "to load properly.",
    "Algorithm;can_train": "If True will train after playing a number of games.",
    "Algorithm;preprocessor.rst": "The name of the preprocessor.rst, that is used to processes the images for "                                  
                                      "the algorithm_base, does have to imported in Algorithm to work correctly. If "                                 
                                      "'None' will return the original image, if 'empty', will destroy the image",

    "AlgorithmSettings;EMPTY": "Add extra variables in case you need them",
    "PreprocessorSettings;EMPTY": "Add extra variables in case you need them",


    # Add the help to the HUMAN players
    "save_highscore": "Not implemented*",
    "keys": "If you render using this app, these are the keys that you can use to controll the game",
    "player": "Just to say that you are a plain old boring human.rst, AI will rule the world... Just wait for it you "
              "unbeliever!!!",

    # Add the help to buttons
    "LOAD AI": "Can be used to load the game settings and an AI from the computer.",
}
