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

    def histogram(self, n):
        trials = [self.simulate() for _ in range(n)]
        bins = range(max(trials) + 1)

        n, bins, patches = plt.hist(
            x=trials, bins=bins, color="#0504aa", alpha=0.7, rwidth=0.85
        )
        plt.grid(axis="y", alpha=0.75)
        plt.xlabel("# Days")
        plt.ylabel("Count")
        title = f"{self.cop.__repr__()} vs {self.robber.__repr__()}"
        plt.title(title)

        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

        plt.show()
