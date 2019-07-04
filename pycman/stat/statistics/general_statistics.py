import pandas as pd


class GeneralStats:
    def __init__(self, file_path):
        self._file_path = file_path
        self.df = pd.read_csv(self._file_path, delimiter="|")

    def summary_stats(self):
        """
        Returns summary statistics over evaluated games
        - Mean and standard deviation of reward
        - Average steps
        -
        """
        pass

    def action_distribution(self):
        """
        Returns a bar chart of the action distribution
        """
        pass
