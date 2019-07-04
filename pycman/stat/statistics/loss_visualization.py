import pandas as pd

# Visualization
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Button, Tk


class LossViz:
    def __init__(self, file_name, figsize=(10, 5)):
        self._file_name = file_name
        self.window = Tk()
        self.fig = Figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        # Initialize main visualization buttons
        self.button = Button(self.window, text="Loss Visualization".center(30),
                             command=self.plot_loss)
        self.button.pack()

        # Auxiliary buttons
        self.save_button = Button(self.window, text="Save Figure".center(30),
                                  command=self.save_figure)
        self.save_button.pack()

        # Initialize Figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()

    def plot_loss(self):
        # Placeholder plot
        self.ax.plot(range(50), range(50)[::-1], color='blue', label="Loss")
        # Format plot
        self.ax.set_title("Loss Over Games", fontsize=16)
        self.ax.set_xlabel("Nr. Games")
        self.ax.set_ylabel("Loss", rotation=0)
        self.ax.legend()
        self.canvas.draw()
        return self

    def save_figure(self):
        """
        Saves the figure currently on display
        """
        self.fig.savefig(f'plot_of_{self._file_name}_loss', dpi=300)
        return self

    def display(self):
        self.window.mainloop()
        return self

if __name__ == "__main__":
    logging_file = "Logging_File_Name"
    loss = LossViz(logging_file)

    # Configure plot manually
    loss.plot_loss()
    loss.save_figure()

    # Configure with GUI
    # loss.display()
