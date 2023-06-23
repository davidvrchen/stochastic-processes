from itertools import chain, permutations
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from .plots import COLORS


def is_transition_matrix(matrix: np.matrix) -> bool:
    """Checks if the matrix is a valid transition matrix,
    i.e. if the rows sum up to 1."""

    return all(np.sum(row) == 1 for row in matrix) and all(
        all(entry >= 0 for entry in row) for row in matrix
    )


Hideout = int
Data = List[int]


class RandomGraphWalker:
    def __init__(self, transition_matrix) -> None:

        assert is_transition_matrix(transition_matrix), "not a valid transition matrix"

        if not isinstance(transition_matrix, np.matrix):
            transition_matrix = np.array(transition_matrix)

        self.transition_matrix = transition_matrix
        self.graph = nx.DiGraph(self.transition_matrix, create_using=nx.DiGraph)

        self.number_of_hideouts = len(self.transition_matrix)
        self.hideouts = np.arange(0, self.number_of_hideouts, 1)

        self.position = None

    def __repr__(self) -> str:
        return "Traverse Blackwater non-uniformly using transition matrix."

    def set_position(self, position):
        """Set the position of the graph walker."""

        self.position = position

    def next_hideout(self) -> Hideout:
        """Return the next house to be surveiled by the sheriff."""

        self.position = np.random.choice(
            self.hideouts, p=self.transition_matrix[self.position]
        )

        return self.position


class Blackwater:
    def __init__(
        self, cop: RandomGraphWalker, robber: RandomGraphWalker, name: str
    ) -> None:
        """Simulates the inhomgeneous transition probabilities."""

        assert (
            cop.number_of_hideouts == robber.number_of_hideouts
        ), "cop and robber have different hideouts"

        self.cop = cop
        self.robber = robber

        self.number_of_hideouts = self.cop.number_of_hideouts

        self.name = name

    def __repr__(self) -> str:
        return "Blackwater, a small town in the Wild West."

    def caught_next_day(self) -> bool:
        """Move both cop and robber and return True if they are in the same house
        otherwise return False."""

        assert (
            self.robber.position != self.cop.position
        ), "cop and robber already in same house"

        watchpost = self.cop.next_hideout()
        hideout = self.robber.next_hideout()

        return hideout == watchpost

    def simulate(self, initial_cop, initial_robber) -> Tuple[int, Hideout]:
        """Set position of both cop and robber, then simulate the
        man-hunt untill the robber is caught."""

        self.cop.set_position(initial_cop)
        self.robber.set_position(initial_robber)

        days = 0

        while not self.caught_next_day():
            days += 1

        # print(self.cop.position + 1)
        return (days, self.cop.position + 1)

    def extract_data(self, initial_cop, initial_robber, trials) -> Tuple[Data, Data]:
        """Extract data on how many days it took for the robber to be caught,
        keep track of where the robber is caught."""

        trials = [self.simulate(initial_cop, initial_robber) for _ in range(trials)]
        days, positions = zip(*trials)
        return days, positions

    def histogram(
        self,
        initial_cop: Hideout,
        initial_robber: Hideout,
        trials: int = 10_000,
        title: bool = False,
        fit: bool = False,
        save: bool = False,
    ):
        """Make a single histogram"""

        days, positions = self.extract_data(initial_cop, initial_robber, trials)

        bins = range(max(days) + 1)
        plt.cla()
        ax = plt.gca()
        n, bins, patches = plt.hist(
            x=days,
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
            title = f"Initial positions; cop: {initial_cop}, robber: {initial_robber}"
            plt.title(title)

        plt.legend()

        if save:
            plt.savefig(
                f"plots/{self.name}/histogram_ic{initial_cop}_ir{initial_robber}.pdf",
                bbox_inches="tight",
            )

        return days, positions

    def caught_in_n_days(
        self,
        n: int = 4,
        initial_cop: Hideout = 0,
        initial_robber: Hideout = 1,
        trials: int = 10_000,
    ) -> float:
        """Calculate the probability of catching the robber in n days."""

        def caught_cnt_rec(n: int):
            if n < 1:
                return False
            elif self.caught_next_day():
                return True
            return caught_cnt_rec(n - 1)

        def init_rec(initial_cop: Hideout, initial_robber: Hideout, n: int):
            """Initialize the recursion to count the number of days."""

            self.cop.set_position(initial_cop)
            self.robber.set_position(initial_robber)

            return caught_cnt_rec(n)

        data = [init_rec(initial_cop, initial_robber, n) for _ in range(trials)]

        return sum(data) / len(data)

    def house_histogram(
        self,
        initial_cop,
        initial_robber,
        positions,
        save: bool,
        clear: bool = True,
    ):
        """Create a histogram showing in which house the robber was caught"""
        if clear:
            plt.cla()

        y = list(range(1, self.number_of_hideouts + 1))
        plt.bar(
            y,
            [positions.count(pos)/len(positions) for pos in y],
            alpha=0.7,
            label="Simulation",
        )

        plt.grid(axis="y", alpha=0.75)
        ax = plt.gca()
        ax.set_xticks([1, 2, 3])
        plt.xlabel("House")
        plt.ylabel("Relative Count")
        plt.legend()
        plt.legend()

        if save:
            plt.savefig(
                f"plots/{self.name}/catching_house_ic{initial_cop}_ir{initial_robber}.pdf",
                bbox_inches="tight",
            )

    def compile_results(self, n: int = 4, save: bool = True, verbose: bool = False):
        """Run all the different simulations and possibly save the results."""

        initial_position_permutations = list(
            permutations(range(self.number_of_hideouts), 2)
        )

        # histograms
        if verbose:
            print("creating histograms")

        combined_days, combined_positions = [], []
        for initial_cop, initial_robber in initial_position_permutations:
            days, positions = self.histogram(
                initial_cop=initial_cop,
                initial_robber=initial_robber,
                save=save,
            )

            combined_days.append(days)
            combined_positions.append(positions)

            if verbose:
                print("...")

        dayss = list(chain(*combined_days))

        bins = range(max(days) + 1)
        plt.cla()
        m, bins, patches = plt.hist(
            x=dayss,
            bins=bins,
            density=True,
            alpha=0.7,
            label="Simulation",
        )

        plt.grid(axis="y", alpha=0.75)
        plt.xlabel("Number Of Days")
        plt.ylabel("Relative Count")
        plt.legend()
        plt.ylim(ymax=m.max() * 1.05)
        plt.legend()

        if save:
            plt.savefig(
                f"plots/{self.name}/histogram_combined.pdf",
                bbox_inches="tight",
            )

        # caught in which house
        if verbose:
            print("processing data to find distribution where robber was caught")

        for i, data in enumerate(combined_positions):
            initial_cop, initial_robber = initial_position_permutations[i]
            self.house_histogram(initial_cop, initial_robber, data, save)

            if verbose:
                print("...")

        positionss = list(chain(*combined_positions))
        plt.cla()
        plt.bar(
            range(1, self.number_of_hideouts + 1),
            np.histogram(positionss, bins=3)[0]
            / np.histogram(positionss, bins=3)[0].sum(),
            alpha=0.7,
            label="Simulation",
        )

        plt.grid(axis="y", alpha=0.75)
        ax = plt.gca()
        ax.set_xticks([1, 2, 3])
        plt.xlabel("House")
        plt.ylabel("Relative Count")
        plt.legend()
        plt.legend()

        if save:
            plt.savefig(
                f"plots/{self.name}/catching_house_combined.pdf",
                bbox_inches="tight",
            )

        # calculate n day, catching probability
        if verbose:
            print(f"calculating {n} day catching probability")

        catching_probabilities = []
        for initial_cop, initial_robber in initial_position_permutations:
            catching_probabilities.append(
                self.caught_in_n_days(
                    n=n, initial_cop=initial_cop, initial_robber=initial_robber
                )
            )

            if verbose:
                print("...")

        catching_probability = np.average(catching_probabilities)
        dataframe = pd.DataFrame(
            {f"{n}_day_catching_probability": catching_probabilities + [catching_probability]}
        )
        dataframe.to_csv(f"plots/{self.name}/{n}_day_catching_probability.csv")

        if verbose:
            print(f"{n} day catching probability is: {catching_probabilities}")
