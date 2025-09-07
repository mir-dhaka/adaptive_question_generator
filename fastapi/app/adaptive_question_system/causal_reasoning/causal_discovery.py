# causal_reasoning/causal_discovery.py

"""
Causal discovery from observational data using constraint-based methods.
"""

import panda as pd
import networkx as nx
from typing import List, Tuple


class CausalDiscovery:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.graph = nx.DiGraph()

    def discover(self) -> nx.DiGraph:
        """
        Dummy causal discovery: builds a graph based on variable correlations.
        In real scenarios, apply PC/FCI or NOTEARS algorithms.
        """
        variables = self.data.columns
        for var1 in variables:
            for var2 in variables:
                if var1 != var2 and self.data[var1].corr(self.data[var2]) > 0.6:
                    self.graph.add_edge(var1, var2)
        return self.graph

    def get_edges(self) -> List[Tuple[str, str]]:
        return list(self.graph.edges)

    def get_graph(self) -> nx.DiGraph:
        return self.graph
