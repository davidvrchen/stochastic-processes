from abc import ABC, abstractmethod
from typing import Tuple

Hideout = int

class SearchStrategy(ABC):
    def __init__(self) -> None:
        pass

    def set_possible_hideouts(self, possible_hideouts):
        self.possible_hideouts = possible_hideouts

    @abstractmethod
    def next_watchpost(self) -> Hideout:
        """Return the next house to surveil for the sheriff.
        """
        pass


class HidingStrategy(ABC):
    def __init__(self) -> None:
        pass


    def set_possible_hideouts(self, possible_hideouts):
        self.possible_hideouts = possible_hideouts


    @abstractmethod 
    def next_hideout(self) -> Hideout:
        """Return the next hideout for the outlaw.
        """
        pass


class Blackwater:
    def __init__(self, sheriff: SearchStrategy, outlaw: HidingStrategy, possible_hideouts: Tuple[Hideout]) -> None:
        self.sheriff = sheriff
        self.outlaw = outlaw
        self.possibel_hideouts = possible_hideouts

        self.sheriff.set_possible_hideouts(possible_hideouts)
        self.outlaw.set_possible_hideouts(possible_hideouts)
        
    def caught_next_day(self) -> bool:
        """Progress one day,
        """

        watchpost = self.sheriff.next_watchpost()
        hideout = self.outlaw.next_hideout()

        if hideout == watchpost:
            return True
        
        return False
        

    def simulate(self) -> int:
        days = 0

        while not self.caught_next_day():
            days += 1

        return days

