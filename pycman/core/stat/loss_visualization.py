# Visualization
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure


class LossViz:
    def __init__(self, file_name, figsize=(10, 5)):
        self._file_name = file_name
        self.losses = []
        self.fig = Figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

    def plot_loss(self, color="Blue", dpi=300):
        """
        Plots the loss over games
        and saves it as a png
        """
        # Placeholder plot
        # TODO Get Loss from Log
        self.ax.plot(range(50), range(50)[::-1], color=color, label="Loss")
        # Format plot
        self.ax.set_title(f"Loss Over Games of '{self._file_name}'", weight="bold", fontsize=20)
        self.ax.set_xlabel("Nr. Games", fontsize=12)
        self.ax.set_ylabel("Loss", fontsize=12, rotation=0)
        self.fig.savefig(f"plot_of_loss_{self._file_name}.png", dpi=dpi)
        return self


if __name__ == "__main__":
    logging_file = "game.log"
    loss = LossViz(logging_file)
    # Configure and save plot
    loss.plot_loss()
