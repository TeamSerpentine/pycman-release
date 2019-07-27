
class Log:

    _line_log = None
    _game_log = None

    def __init__(self, _file_name: str, id=None):
        if id is not None:
            self._file_name = _file_name + '-' + str(id) + '.csv'
        else:
            self._file_name = _file_name + '.csv'

    def line(self, *args):
        """Writes data to a single line. """
        if self._line_log is None:
            self._line_log = open(self._file_name, "w+")

        self._line_log.write(";".join([str(x) for x in args])+'\n')

    # def game(self, *args):
    #     """Writes all the logged values for a particular game to a single line. """
    #     # TODO: Needs implementation
    #     pass

        # if self._game_log is None:
        #     self._game_log = open(self._file_name, "w+")
        #
        # self._game_log.write(";".join([str(x) for x in args]) + '\n'  )

    def close(self):
        if self._line_log is not None:
            self._line_log.close()
        if self._game_log is not None:
            self._game_log.close()
