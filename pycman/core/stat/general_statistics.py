import os
import json
import numpy as np

# Visualization
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class GeneralStats:
    def __init__(self, file_name):
        self._file_name = file_name
        # TODO Fix path of logs
        self.log = list(open(f"{os.getcwd()}/{self._file_name}"))
        # TODO Clean up self.game
        self.game = [line.split(" ") for line in self.log][0][0].split('-')[0]
        self.reward = [json.loads(line.split(";")[-1])['reward'] for line in self.log]
        self.actions = [json.loads(line.split(";")[-1])['action'] for line in self.log]
        self.action_dist = np.sum(self.actions, axis=0)
        # self.action_dist = [12, 10]
        self.total_actions = np.sum(self.action_dist)
        # Normalize actions
        self.action_dist = self.action_dist / self.total_actions if self.total_actions else np.zeros(len(self.action_dist))
        self.action_dist *= 100

    def summary_stats(self):
        """
        Returns summary statistics over evaluated games
        - Game
        - Total games played
        - Mean and standard deviation of Reward
        - Total actions taken
        - Most picked action
        - % most picked action of all actions
        """
        mean_reward = np.mean(self.reward)
        std_reward = np.std(self.reward)
        pop_action = np.argmax(self.action_dist)
        games_played = len(self.actions)

        return f"       Summary For '{self._file_name}':\n\n\
        Game: {self.game}\n\
        Total Games Played: {games_played}\n\
        Mean Reward: {'{:.5n}'.format(mean_reward)}\n\
        Std Reward: {'{:.5n}'.format(std_reward)}\n\
        Total Actions Taken: {self.total_actions}\n\
        Most picked action: {pop_action}, chosen {'{:.5n}'.format(self.action_dist[pop_action])} % of the time"

    def plot_action_distribution(self, dpi=300):
        """
        Saves a bar chart of the action distribution
        """
        plt.bar(x=range(len(self.action_dist)), height=self.action_dist, color=[*'bgrymckw'])
        plt.title(f"Action Distribution Of '{self._file_name}'", weight="bold", fontsize=20)
        plt.xlabel("Actions", fontsize=16)
        plt.xticks(range(len(self.action_dist)), fontsize=14)
        plt.yticks(fontsize=14)
        plt.ylabel("% of total actions", fontsize=16)
        plt.tight_layout()
        plt.savefig(f"action_distribution_of_{self._file_name}.png", dpi=dpi)


if __name__ == "__main__":
    file = "game.log"
    stats = GeneralStats(file)
    # Configure and save plot
    stats.plot_action_distribution()
    # Print summary statistics
    print(stats.summary_stats())
