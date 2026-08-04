import matplotlib.pyplot as plt


def plot_lines(
    curves,
    xlabel="Steps",
    ylabel="Value",
    title=None,
    figsize=(8, 5)
):
    """
    Plot multiple line charts.

    Parameters:
        curves: list of tuples
            [(y1, label1), (y2, label2), ...]
        xlabel: str
        ylabel: str
        title: str
        figsize: tuple
    """

    plt.figure(figsize=figsize)

    for y, label in curves:
        plt.plot(
            y,
            label=label
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if title:
        plt.title(title)

    plt.legend()
    plt.grid(True)

    plt.show()