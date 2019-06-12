"""
    Date created: 2019/03/15
    Python Version: 3.7
    License: MIT License

    Take a look at the pycman repository or the MIT license for more information on the use and reuse of pycman.
"""


class Windows:
    @staticmethod
    def set_logos(path):
        return f"{path}/serpentine.ico", f"{path}/serpentine_160x90.gif"


class Linux:
    @staticmethod
    def set_logos(path):
        return f"{path}/serpentine.ppm", f"{path}/serpentine_160x90.gif"


class Darwin:
    @staticmethod
    def set_logos(path):
        return f"{path}/serpentine.ppm", f"{path}/serpentine_160x90.gif"


if __name__ == "__main__":
    pass
