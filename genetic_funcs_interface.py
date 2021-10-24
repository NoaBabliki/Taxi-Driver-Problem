from dataclasses import dataclass
from typing import Callable, Tuple

Coordinate = Tuple[int, int]
Station = Tuple[Coordinate, int, bool]  # coordiate, ID, is_destination
Solution = Tuple[Station]


@dataclass
class GeneticFuncsInterface:
    crossover: Callable[[Solution, Solution, float], Tuple[Solution, Solution]]
    mutation: Callable[[Solution, float], Solution]
