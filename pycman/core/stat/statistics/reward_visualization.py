import os
import json
import itertools
import pandas as pd

# Visualization
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Checkbutton, Button, Tk

# Specify color map
colors = itertools.cycle([*'brgcmykw'])


class RewardViz:
    def __init__(self, file_name, figsize=(10, 5)):
        self._file_name = file_name
        # TODO Fix Path of logs
        self.log = list(open(f"{os.getcwd()}/{self._file_name}"))
        self.game = [line.split(" ") for line in self.log][0][0]
        self.reward = [json.loads(line.split(";")[-1])['reward'] for line in self.log]
        self.baselines = pd.read_csv('deep_rl_scores.csv')
        self.window = Tk()
        self.fig = Figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        # Initialize main visualization buttons
        self.button = Button(self.window, text="Reward Visualization".center(30),
                             command=self.plot_reward)
        self.button.grid(row=0, column=0)

        # Initialize baseline check buttons
        for num, name in enumerate(self.baselines.columns[1:]):
            setattr(self, name, Checkbutton(self.window, text=f"{name} Baseline".center(20),
                                            command=self.lambda_func(name)))
            getattr(self, name).grid(row=num, column=1)

        # Auxiliary buttons
        self.save_button = Button(self.window, text="Save Figure".center(30),
                                  command=self.save_figure)
        self.save_button.grid(row=10, column=0)

        # Initialize Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=9, column=0)

    def lambda_func(self, name):
        """
        Fix for setting attributes
        of Baseline Checkbuttons
        """
        return lambda: self.plot_baseline(name)

    def plot_reward(self):
        """
        Plots the reward over games
        and adds it to the GUI
        """
        self.ax.plot(range(len(self.reward)), self.reward, color=next(colors), label="Reward")
        # Format plot
        self.ax.set_title(f"Reward Over Games of '{self._file_name}'", weight="bold", fontsize=20)
        self.ax.set_xlabel('Nr. Games', fontsize=12)
        self.ax.set_ylabel('Reward', fontsize=12, rotation=0)
        self.ax.legend()
        self.canvas.draw()
        return self

    def plot_baseline(self, selection):
        """
        Plots a horizontal line
        from a registered algorithm
        and adds it to the GUI

        Sources for baselines: https://arxiv.org/pdf/1602.01783.pdf
        and https://arxiv.org/pdf/1602.04621.pdf
        """
        # TODO Fix unchecking of boxes
        # TODO Fix if baseline of env is not available
        score = self.baselines[self.baselines['Game'] == self.game][selection]
        self.ax.hlines(score, 0, len(self.reward),
                       label=f"{selection} baseline",
                       linestyle='dotted', color=next(colors))
        self.ax.legend()
        self.canvas.draw()
        return self

    def save_figure(self, dpi=300):
        """
        Saves the figure currently on display
        """
        self.fig.savefig(f'plot_of_{self._file_name}_reward.png', dpi=dpi)
        return self

    def display(self):
        """
        Launches the GUI
        """
        self.window.mainloop()
        return self


if __name__ == '__main__':
    logging_file = "game.log.1"
    reward = RewardViz(logging_file)

    # Configure plot manually
    reward.plot_reward()
    reward.plot_baseline("DDQN")
    reward.plot_baseline("A3C LSTM")
    reward.save_figure()

    # Configure with GUI
    # reward.display()
