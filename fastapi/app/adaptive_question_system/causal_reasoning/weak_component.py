# causal_reasoning/weak_component.py

"""
Identifies weakly connected components in the causal graph to support
modular diagnostics or intervention.
"""

import networkx as nx
from typing import List


class WeakComponentAnalyzer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph

    def get_weakly_connected_components(self) -> List[List[str]]:
        """
        Returns a list of weakly connected components as lists of nodes.
        """
        components = list(nx.weakly_connected_components(self.graph))
        return [list(component) for component in components]

    def print_components(self):
        components = self.get_weakly_connected_components()
        for idx, comp in enumerate(components, 1):
            print(f"Component {idx}: {comp}")
