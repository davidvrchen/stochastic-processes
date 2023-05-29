import networkx as nx
import numpy as np

from utils.graph_based import Blackwater, RandomGraphWalker
import utils.plots


# transition_matrix_cop = [[0.4, 0.6], [0.1, 0.9]]
# transition_matrix_robber = [[0.4, 0.6], [0.1, 0.9]]

n=3
transition_matrix_cop = [[1/n for _ in range(n)] for _ in range(n)]
transition_matrix_robber = [[1/n for _ in range(n)] for _ in range(n)]

if __name__ == "__main__":

    cop = RandomGraphWalker(transition_matrix=transition_matrix_cop)
    robber = RandomGraphWalker(transition_matrix=transition_matrix_robber)

    blackwater = Blackwater(cop=cop, robber=robber)

    blackwater.histogram(100)
