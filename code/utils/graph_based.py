import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from .plots import COLORS

Hideout = int


def is_transition_matrix(matrix: np.matrix) -> bool:
    """Checks if the matrix is a valid transition matrix,
    i.e. if the rows sum up to 1."""

    return all(np.sum(row) == 1 for row in matrix)


class RandomGraphWalker:
    def __init__(self, transition_matrix) -> None:

        assert is_transition_matrix(transition_matrix), "not a valid transition matrix"

        if type(transition_matrix) != np.matrix:
            transition_matrix = np.array(transition_matrix)

        self.transition_matrix = transition_matrix
        self.graph = nx.DiGraph(self.transition_matrix, create_using=nx.DiGraph)

        self.number_of_hideouts = len(self.transition_matrix)
        self.hideouts = np.arange(0, self.number_of_hideouts, 1)
        self.position = np.random.randint(0, self.number_of_hideouts - 1)

    def __repr__(self) -> str:
        return "Traverse Blackwater non-uniformly using transition matrix."

    def next_hideout(self) -> Hideout:
        """Return the next house to be surveiled by the sheriff."""
        self.position = np.random.choice(
            self.hideouts, p=self.transition_matrix[self.position]
        )

        return self.position


class Blackwater:
    def __init__(
        self,
        cop: RandomGraphWalker,
        robber: RandomGraphWalker,
    ) -> None:
        """Simulates the inhomgeneous transition probabilities."""

        assert (
            cop.number_of_hideouts == robber.number_of_hideouts
        ), "cop and robber have different hideouts"

        self.cop = cop
        self.robber = robber

    def __repr__(self) -> str:
        return "Blackwater, a small town in the Wild West."

    def caught_next_day(self) -> bool:
        """Progress one day."""

        watchpost = self.cop.next_hideout()
        hideout = self.robber.next_hideout()

        if hideout == watchpost:
            return True

        return False

    def simulate(self) -> int:
        days = 0

        while not self.caught_next_day():
            days += 1

        return days

    def histogram(self, trials, title: bool = False, fit: bool = False):
        trials = [self.simulate() for _ in range(trials)]
        bins = range(max(trials) + 1)

        ax = plt.gca()

        n, bins, patches = plt.hist(
            x=trials,
            bins=bins,
            density=True,
            alpha=0.7,
            label="Simulation",
        )

        plt.grid(axis="y", alpha=0.75)
        plt.xlabel("Number Of Days")
        plt.ylabel("Relative Count")
        plt.legend()
        plt.ylim(ymax=n.max() * 1.05)

        if fit:

            def geo_dist(days, n):
                p = 1 / n
                return p * np.power(1 - p, days)

            ax = plt.gca()

            ax.plot(
                bins + 0.5,
                geo_dist(bins, self.cop.number_of_hideouts),
                color=COLORS[2],
                linestyle="",
                marker="o",
                label="Geometric distribution",
            )

        if title:
            title = f"{self.cop.__repr__()} vs {self.robber.__repr__()}"
            plt.title(title)

        plt.show()
