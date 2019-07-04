import numpy as np
import pandas as pd


class GeneralStats:
    def __init__(self):
        self.df = pd.read_csv("logging_file", delimiter="|")

    def summary_stats(self):
        pass

    def action_distribution(self):
        pass
