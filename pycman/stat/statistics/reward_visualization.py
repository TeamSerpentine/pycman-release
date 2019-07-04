import pandas as pd

# Visualization
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import Checkbutton, Button, Tk


class RewardViz:
    def __init__(self, file_name):
        self._filename = file_name
        # self.df = pd.read_csv("Logging File", delimiter="|")
        self.baselines = pd.read_csv('deep_rl_scores.csv')
        self.window = Tk()
        self.fig = Figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot(111)

        self.button = Button(self.window, text="Reward Visualization".center(30),
                             command=self.plot_reward)
        self.button.grid(row=0, column=0)

        self.human_button = Checkbutton(self.window, text="Human Baseline".center(30),
                                        command=lambda: self.plot_baseline("Human"))
        self.human_button.grid(row=0, column=1)

        self.random_button = Checkbutton(self.window, text="Random Baseline".center(30),
                                         command=lambda: self.plot_baseline("Random"))
        self.random_button.grid(row=1, column=1)

        self.dqn_button = Checkbutton(self.window, text="DQN Baseline".center(30),
                                      command=lambda: self.plot_baseline("DQN"))
        self.dqn_button.grid(row=2, column=1)

        self.ddqn_button = Checkbutton(self.window, text="DDQN Baseline".center(30),
                                       command=lambda: self.plot_baseline("DDQN"))
        self.ddqn_button.grid(row=3, column=1)

        self.duelingdqn_button = Checkbutton(self.window, text="Dueling DQN Baseline".center(30),
                                             command=lambda: self.plot_baseline("Dueling DQN"))
        self.duelingdqn_button.grid(row=4, column=1)

        self.a3cff_button = Checkbutton(self.window, text="A3C Feed Forward Baseline".center(30),
                                        command=lambda: self.plot_baseline("A3C FF"))
        self.a3cff_button.grid(row=5, column=1)

        self.a3clstm_button = Checkbutton(self.window, text="A3C LSTM Baseline".center(30),
                                          command=lambda: self.plot_baseline("A3C LSTM"))
        self.a3clstm_button.grid(row=6, column=1)

        self.save_button = Button(self.window, text="Save Figure".center(30),
                                  command=self.save_figure)
        self.save_button.grid(row=8, column=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=7, column=0)

    def plot_reward(self):
        # Placeholder plot
        self.ax.plot(range(5), [1, 5, 8, 4, 23], color='blue', label=f"Reward")
        # Format plot
        self.ax.set_title("Reward Over Games", fontsize=16)
        self.ax.set_xlabel('Nr. Games')
        self.ax.set_ylabel('Reward', rotation=0)
        self.ax.legend()
        self.canvas.draw()
        return self

    def plot_baseline(self, selection):
        game = 'Pong'  # TODO Take from Logging File
        score = self.baselines[self.baselines['Game'] == game][selection]
        self.ax.hlines(score, 0, 5, label=f"{selection} baseline")
        self.ax.legend()
        self.canvas.draw()
        return self

    def save_figure(self):
        self.fig.savefig(f'plot_of_{self._filename}_reward', dpi=300)
        return self

    def display(self):
        self.window.mainloop()
        return self


if __name__ == '__main__':
    logging_file = "Logging_File_Name"
    reward = RewardViz(logging_file)
    reward.display()

