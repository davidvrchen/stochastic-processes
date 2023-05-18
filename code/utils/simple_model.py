from abc import ABC, abstractmethod
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

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

    def histogram(self, n):
        trials = [self.simulate() for _ in range(n)]
        bins = range(max(trials) + 1)

        n, bins, patches = plt.hist(
            x=trials, bins=bins, color="#0504aa", alpha=0.7, rwidth=0.85
        )
        plt.grid(axis="y", alpha=0.75)
        plt.xlabel("# Days")
        plt.ylabel("Count")
        title = f"{self.sheriff.__repr__()} vs {self.robber.__repr__()}"
        plt.title(title)

        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

        plt.show()
