import random
from typing import Tuple

from utils.simple_model import (Blackwater, Hideout, HidingStrategy,
                                SearchStrategy)


class RandomSearch(SearchStrategy):
    def next_watchpost(self) -> Hideout:
        """Randomly chooses one of the possible hideouts to surveil next.
        """

        return random.choice(self.possible_hideouts)
    
    
    def __repr__(self) -> str:
        return "Random search strategy"


class PickOneAndHide(HidingStrategy):
    def __init__(self, possible_hideouts) -> None:
        super().__init__(possible_hideouts)
        self.hideout = random.choice(self.possible_hideouts)


    def next_hideout(self) -> Hideout:
        """Pick hiding location and always hide there.
        """
        
        return self.hideout
    

    def __repr__(self) -> str:
        return f"Pick one and hide strategy (hiding at {self.hideout})"


class RandomHiding(HidingStrategy):
    def next_hideout(self) -> Hideout:
        """Return a randomly chosen hideout evey time.
        """

        return random.choice(self.possible_hideouts)
    

    def __repr__(self) -> str:
        return "Random hiding strategy"


if __name__ == "__main__":

    hideouts = (1, 2, 3, 4, 5)

    blackwater1 = Blackwater(RandomSearch, PickOneAndHide, possible_hideouts=hideouts)
    blackwater2 = Blackwater(RandomSearch, RandomHiding, possible_hideouts=hideouts)

    blackwater1.histogram(10_000)
    blackwater2.histogram(10_000)
