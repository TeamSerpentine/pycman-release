
import logging
import json


class Collector:
    def __init__(self):
        self.store = []

    def set(self, item):
        self.store = item

    def add(self, item):
        if not hasattr(item, "__iter__"):
            item = [item]
        self.store.extend(item)

    def __replace(self, new_agents):
        self.store = new_agents

    def __str__(self):
        return str(self.store)

    def __repr__(self):
        return f"<class '{Collector.__name__}'>"

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)





class DataLogger:
    def __init__(self, log_name):
        self.data = dict()
        self.log_name = log_name
        self.log = logging.getLogger(log_name)

    def add(self, item: dict):
        for k, v in item.items():
            self.data[k] = v

    def json(self):
        return json.dumps(self.data)
