from abc import ABC, abstractmethod
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from .plots import COLORS

Hideout = int


class SearchStrategy(ABC):
    def __init__(self, possible_hideouts) -> None:
        self.possible_hideouts = possible_hideouts

    @abstractmethod
    def next_watchpost(self) -> Hideout:
        """Return the next house to be surveiled by the sheriff."""

    def __repr__(self) -> str:
        return "Base class for the sheriff searching strategy."


class HidingStrategy(ABC):
    def __init__(self, possible_hideouts) -> None:
        self.possible_hideouts = possible_hideouts

    def __repr__(self) -> str:
        return "Base class for the robber hiding strategy."

    @abstractmethod
    def next_hideout(self) -> Hideout:
        """Return the next hideout for the robber."""


class Blackwater:
    def __init__(
        self,
        sheriff_strategy: SearchStrategy,
        robber_strategy: HidingStrategy,
        possible_hideouts: Tuple[Hideout],
    ) -> None:

        self.sheriff = sheriff_strategy(possible_hideouts)
        self.robber = robber_strategy(possible_hideouts)
        self.possibel_hideouts = possible_hideouts

    def __repr__(self) -> str:
        return "Blackwater, a small town in the Wild West."

    def caught_next_day(self) -> bool:
        """Progress one day."""

        watchpost = self.sheriff.next_watchpost()
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
                geo_dist(bins, len(self.possibel_hideouts)),
                color=COLORS[2],
                linestyle="",
                marker="o",
                label="Geometric distribution",
            )

        if title:
            title = f"{self.sheriff.__repr__()} vs {self.robber.__repr__()}"
            plt.title(title)

    def histogram_detailed(self, n, save: str = None) -> None:
        """Histogram with theoretical distribution juxtaposed on it.
        save is the name with which to save the plot. Stored in plots/....
        """

        plt.figure(figsize=(8, 8))

        self.histogram(n)

        if save is not None:
            filename = f"plots/{save}.pdf"

            plt.savefig(filename, bbox_inches="tight")


class Compare:
    def __init__(self, blackwater1: Blackwater, blackwater2: Blackwater) -> None:
        self.exp1 = blackwater1
        self.exp2 = blackwater2

    def hist(self, n, save: str = None) -> None:
        plt.figure(figsize=(8, 8))

        trials1 = [self.exp1.simulate() for _ in range(n)]
        trials2 = [self.exp2.simulate() for _ in range(n)]
        
        
        bins1 = range(max(trials1) + 1)
        bins2 = range(max(trials2) + 1)

        ax = plt.gca()

        n1, bins1, patches1 = plt.hist(
            x=trials1,
            bins=bins1,
            density=True,
            color=COLORS[1],
            alpha=0.6,
            label="Simple",
        )
        n2, bins2, patches2 = plt.hist(
            x=trials2,
            bins=bins2,
            density=True,
            color=COLORS[2],
            alpha=0.4,
            label="Both Random",
        )

        plt.grid(axis="y", alpha=0.75)
        plt.xlabel("Number Of Days")
        plt.ylabel("Relative Count")
        plt.legend()
        plt.ylim(ymax=max(n1.max(), n2.max()) * 1.05)



        if save is not None:
            filename = f"plots/{save}.pdf"

            plt.savefig(filename, bbox_inches="tight")
