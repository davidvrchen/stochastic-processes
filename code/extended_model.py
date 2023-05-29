import networkx as nx
import numpy as np

from utils.graph_based import Blackwater, RandomGraphWalker
import utils.plots


# transition_matrix_cop = [[0.4, 0.6], [0.1, 0.9]]
# transition_matrix_robber = [[0.4, 0.6], [0.1, 0.9]]


def uniform_matrix(number_of_hideouts):
    """Generates a transition matrix with uniform transition
    probabilities over number_of_hideouts hideouts.
    """

    return [
        [1 / number_of_hideouts for _ in range(number_of_hideouts)]
        for _ in range(number_of_hideouts)
    ]


n = 3
transition_matrix_cop = uniform_matrix(n)
transition_matrix_robber = uniform_matrix(n)

if __name__ == "__main__":

    cop = RandomGraphWalker(transition_matrix=transition_matrix_cop)
    robber = RandomGraphWalker(transition_matrix=transition_matrix_robber)

    blackwater = Blackwater(cop=cop, robber=robber)

    blackwater.histogram(10_000, fit=True)
