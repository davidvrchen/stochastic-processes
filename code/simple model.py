import random

from utils.uniform import Blackwater, Hideout, HidingStrategy, SearchStrategy, Compare
import utils.plots


class RandomSearch(SearchStrategy):
    def next_watchpost(self) -> Hideout:
        """Randomly chooses one of the possible hideouts to surveil next."""

        return random.choice(self.possible_hideouts)

    def __repr__(self) -> str:
        return "Random search strategy"


class ConstantObservation(SearchStrategy):
    def __init__(self, possible_hideouts) -> None:
        super().__init__(possible_hideouts)
        self.hideout = random.choice(self.possible_hideouts)

    def next_watchpost(self) -> Hideout:
        """Watches the same home everyday."""

        return self.hideout

    def __repr__(self) -> str:
        return "Constant observation strategy."


class PickOneAndHide(HidingStrategy):
    def __init__(self, possible_hideouts) -> None:
        super().__init__(possible_hideouts)
        self.hideout = random.choice(self.possible_hideouts)

    def next_hideout(self) -> Hideout:
        """Pick hiding location and always hide there."""

        return self.hideout

    def __repr__(self) -> str:
        return f"Pick one and hide strategy (hiding at {self.hideout})"


class RandomHiding(HidingStrategy):
    def next_hideout(self) -> Hideout:
        """Return a randomly chosen hideout evey time."""

        return random.choice(self.possible_hideouts)

    def __repr__(self) -> str:
        return "Random hiding strategy"


if __name__ == "__main__":

    hideouts = (1, 2, 3, 4)

    blackwater1 = Blackwater(
        ConstantObservation, RandomHiding, possible_hideouts=hideouts
    )
    blackwater2 = Blackwater(RandomSearch, RandomHiding, possible_hideouts=hideouts)

    comparison = Compare(blackwater1, blackwater2)
    comparison.hist(1_000_000, 'symmetry2')
