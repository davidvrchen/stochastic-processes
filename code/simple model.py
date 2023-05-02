import random
from typing import Tuple

from utils.simple_model import Blackwater, HidingStrategy, SearchStrategy, Hideout


hideouts = (1, 2, 3, 4, 5)

class RandomSearch(SearchStrategy):
    def next_watchpost(self) -> Hideout:
        """Randomly chooses one of the possible hideouts to surveil next.
        """
       
        return random.choice(self.possible_hideouts)
    

class PickOneAndHide(HidingStrategy):
     def next_hideout(self) -> Hideout:
        """Return the hideout (determined during the initialization).
        """

        try:
            return self.hideout
        except AttributeError:
            self.hideout = random.choice(self.possible_hideouts)
            return self.hideout
    

sheriff = RandomSearch()
outlaw = PickOneAndHide()
blackwater = Blackwater(sheriff, outlaw, possible_hideouts=hideouts)
print(blackwater.simulate())
