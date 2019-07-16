
import logging
import json


class GlobalAgentSet:
    """ Global collection of agent instances. """

    def __init__(self):
        self.store = []
        self.nested_store = []

    def add(self, item):
        if not isinstance(item, list):
            raise TypeError("Agent must be contained inside a list!")
        self.nested_store.append(item)

    def _get_complex_index(self, idx):
        nr = 0  # elements seen
        i = 0   # list index
        while i < len(self.nested_store) and nr + len(self.nested_store[i]) <= idx:
            nr += len(self.nested_store[i])
            i = i + 1
        j = idx - nr                # element from the ith list
        return i, j

    def __setitem__(self, idx, val):
        i, j = self._get_complex_index(idx)
        self.nested_store[i][j] = val

    def __getitem__(self, idx):
        i, j = self._get_complex_index(idx)
        return self.nested_store[i][j]

    def __str__(self):
        return str(self.store)

    def __repr__(self):
        return f"<class '{GlobalAgentSet.__name__}'>"

    def __iter__(self):
        return iter([agent for agents in self.nested_store for agent in agents])

    def __len__(self):
        return len([agent for agents in self.nested_store for agent in agents])


class DataLogger:
    def __init__(self, log_name):
        self.data = dict()
        self.log_name = log_name
        self.log = logging.getLogger(log_name)

    def add(self, item: dict):
        for k, v in item.items():
            self.data[k] = v

    def json(self):
        self.log = logging.getLogger(self.log_name)
        return json.dumps(self.data)
