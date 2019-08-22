import os


class _Log:
    """Logging class for pycman. It exists in a global namespace."""

    def __init__(self, env, _file_name: str, id=None):
        self._env = env # TODO: Use for future logging improvements!

        if id is not None:
            self._file_name = _file_name + '-' + str(id) + '.csv'
        else:
            self._file_name = _file_name + '.csv'

    def set_header(self, caller, *args):
        """"Sets the header names. """
        if not os.path.isfile(self._file_name):
            with open(self._file_name, "a+") as log_file:
                log_file.write("agent_id;" + ";".join([str(x) for x in args]) + '\n')
        else:
            print("Warning: Can not set the headers because the file already exists!")

    def line(self, caller, *args):
        """Writes data to a single line. """
        if caller.part_of_parallel_pool:
            self._parallel_line(caller, *args)
            return

        with open(self._file_name, "a+") as log_file:
            log_file.write(str(caller.agent_id) + ";" + ";".join([str(x) for x in args]) + '\n')

    def _open_last(self):
        self._line_log = open(self._file_name, "a+")
        # FIXME: FIX THIS FOR PARALLEL

    def _parallel_line(self, caller, *args):
        """Writes data to a single line. """
        # if caller is None:
        #     raise AttributeError("One must specify the calling agent (caller=None) when performing a parallel run.")

        with open(self._file_name[:-4] + str(id(caller)) + '.csv', "a+") as log_file:
            log_file.write(str(caller.agent_id)+";"+";".join([str(x) for x in args])+'\n')


# class ParallelLog():
#
#     _line_logs = []
#     _callers = []
#
#     def __init__(self, _file_name: str):
#         self._file_name = _file_name
#
#     def line(self, caller, *args):
#         """Writes data to a single line. """
#         caller = id(caller)
#         if caller not in self._callers:
#             self._line_logs.append(open(self._file_name + str(caller) + '.csv', "w+"))
#             self._callers.append(caller)
#             print("nr of callers", len(self._callers))
#
#         idx = self._callers.index(caller)
#
#         self._line_logs[idx].write(";".join([str(x) for x in args])+'\n')
#
#     def close(self):
#         for file in self._line_logs:
#             file.close()
#         # TODO: Recombine files
#
#
# class MultiLog():
#
#     file = None
#
#     def line(self, caller, *args):
#         """Writes data to a single line. """
#         if self.file is None:
#             self.file = open("multi" + str(id(caller)) + '.csv', 'w+')
#
#         self.file.write(";".join([str(x) for x in args])+'\n')
#
#     def close(self):
#         if self.file is not None:
#             self.file.close()
#             self.file = None
