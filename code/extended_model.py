import networkx as nx
import numpy as np

import utils.plots
from utils.graph_based import Blackwater, RandomGraphWalker


def uniform_matrix(number_of_hideouts):
    """Generates a transition matrix with uniform transition
    probabilities over number_of_hideouts hideouts.
    """

    return [
        [1 / number_of_hideouts for _ in range(number_of_hideouts)]
        for _ in range(number_of_hideouts)
    ]


R = [[0.1, 0.4, 0.5], [0.3, 0.3, 0.4], [0.1, 0.1, 0.8]]

FIXED = np.identity(3)

UNIFORM = uniform_matrix(3)

RANDOM = [[0.3, 0.2, 0.5], [0.3, 0.2, 0.5], [0.3, 0.2, 0.5]]

ARG_MAX = [[0, 0, 1], [0, 0, 1], [0, 0, 1]]

STATIONARY_DISTRIBUTION = [
    [10 / 74, 13 / 74, 51 / 74],
    [10 / 74, 13 / 74, 51 / 74],
    [10 / 74, 13 / 74, 51 / 74],
]


if __name__ == "__main__":

    robber = RandomGraphWalker(transition_matrix=R)

    cop_uniform = RandomGraphWalker(transition_matrix=UNIFORM)
    cop_copy_robber = RandomGraphWalker(transition_matrix=R)
    cop_random = RandomGraphWalker(transition_matrix=RANDOM)
    cop_argmax = RandomGraphWalker(transition_matrix=ARG_MAX)
    cop_stationary_distr = RandomGraphWalker(transition_matrix=STATIONARY_DISTRIBUTION)

    blackwater_uniform = Blackwater(cop=cop_uniform, robber=robber, name="uniform")
    blackwater_copy_robber = Blackwater(cop=cop_copy_robber, robber=robber, name="copy_robber")
    blackwater_random = Blackwater(cop=cop_random, robber=robber, name="random")
    blackwater_argmax = Blackwater(cop=cop_argmax, robber=robber, name="argmax")
    blackwater_stationary_distr = Blackwater(cop=cop_stationary_distr, robber=robber, name="stationary_distr")

    blackwater_uniform.compile_results(save=True, verbose=False)
    blackwater_copy_robber.compile_results(save=True, verbose=False)
    blackwater_random.compile_results(save=True, verbose=False)
    blackwater_argmax.compile_results(save=True, verbose=False)
    blackwater_stationary_distr.compile_results(save=True, verbose=False)
