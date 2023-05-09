import random
from typing import Tuple

from utils.simple_model import (Blackwater, Hideout, HidingStrategy,
                                SearchStrategy)


class RandomSearch(SearchStrategy):
    def next_watchpost(self) -> Hideout:
        """Randomly chooses one of the possible hideouts to surveil next.
        """

        return random.choice(self.possible_hideouts)


class PickOneAndHide(HidingStrategy):
    def next_hideout(self) -> Hideout:
        """Pick hiding location and always hide there.
        """

        try:
            return self.hideout

        except AttributeError:
            self.hideout = random.choice(self.possible_hideouts)
            return self.hideout


class RandomHiding(HidingStrategy):
    def next_hideout(self) -> Hideout:
        """Return a randomly chosen hideout evey time.
        """

        return random.choice(self.possible_hideouts)


if __name__ == "__main__":

    hideouts = (1, 2, 3, 4, 5)

    sheriff = RandomSearch
    outlaw = PickOneAndHide
    blackwater = Blackwater(sheriff, outlaw, possible_hideouts=hideouts)

    print(blackwater.simulate())
    blackwater.histogram(100_000)
