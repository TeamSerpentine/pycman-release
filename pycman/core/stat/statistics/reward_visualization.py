import pandas as pd

# Visualization
import itertools
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Checkbutton, Button, Tk

matplotlib.use("TkAgg")

# Specify color map
colors = itertools.cycle(['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w'])


# TODO Fix unchecking of boxes
class RewardViz:
    def __init__(self, file_name, figsize=(10, 5)):
        self._file_name = file_name
        # self.df = pd.read_csv(self._file_name, delimiter="|")
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
        self.save_button.grid(row=9, column=0)

        # Initialize Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=8, column=0)

    def lambda_func(self, name):
        return lambda: self.plot_baseline(name)

    def plot_reward(self):
        # Placeholder plot
        self.ax.plot(range(5), [1, 5, 8, 4, 23], color=next(colors), label="Reward")
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
        self.ax.hlines(score, 0, 5, label=f"{selection} baseline", linestyle='dotted', color=next(colors))
        # lines.set_color(cm(len(self.ax.lines) // 3 * 3.0 / NUM_COLORS))
        self.ax.legend()
        self.canvas.draw()
        return self

    def save_figure(self, dpi=300):
        """
        Saves the figure currently on display
        """
        self.fig.savefig(f'plot_of_{self._file_name}_reward', dpi=dpi)
        return self

    def display(self):
        self.window.mainloop()
        return self


if __name__ == '__main__':
    logging_file = "Logging_File_Name"
    reward = RewardViz(logging_file)

    # Configure plot manually
    # reward.plot_reward()
    # reward.plot_baseline("DDQN")
    # reward.plot_baseline("A3C LSTM")
    # reward.save_figure()

    # Configure with GUI
    reward.display()
