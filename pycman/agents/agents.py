""" This file contains the functionality required to add agents to the created environments """

class Agents:
    def __init__(self):
        self._agents = []

    def add(self, step_functie):
        """"Adds an agents with the specified step function. """
        self._agents.append(step_functie)

