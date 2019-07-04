import os
import json
import numpy as np
import pandas as pd

# Visualization
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class GeneralStats:
    def __init__(self, file_name):
        self._file_name = file_name
        self.log = list(open(f"{os.getcwd()}/{self._file_name}"))
        self.game = [line.split(" ") for line in self.log][0][0]
        self.actions = [json.loads(line.split(";")[-1])['actions'] for line in self.log]
        self.action_dist = np.sum(self.actions, axis=0)
        # self.action_dist = [12, 10]
        self.total_actions = np.sum(self.action_dist)
        # Normalize actions
        self.action_dist = self.action_dist / self.total_actions if self.total_actions else np.zeros(len(self.action_dist))
        self.action_dist *= 100

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
        Saves a bar chart of the action distribution
        """
        plt.bar(x=range(len(self.action_dist)), height=self.action_dist)
        plt.title(f"Action Distribution Of {self._file_name}", weight="bold", fontsize=20)
        plt.xlabel("Actions", fontsize=16)
        plt.xticks(range(len(self.action_dist)), fontsize=14)
        plt.yticks(fontsize=14)
        plt.ylabel("% of total actions", fontsize=16)
        plt.tight_layout()
        plt.savefig(f"action_distribution_of_{self._file_name}.png", dpi=300)


if __name__ == "__main__":
    file_name = "game.log.1"
    stats = GeneralStats(file_name)
    stats.action_distribution()
