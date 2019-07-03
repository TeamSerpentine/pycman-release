
class Collecter:
    def __init__(self):
        self.store = []

    def add(self, item):
        if not hasattr(item, "__iter__"):
            item = [item]
        self.store.extend(item)

    def __repr__(self):
        return str(self.store)

    def __iter__(self):
        return iter(self.store)
