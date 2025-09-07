# knowledge_model/dag_model.py

"""
Defines a directed acyclic graph (DAG) to model concept dependencies.
"""

import networkx as nx
from typing import List, Tuple


class KnowledgeDAG:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_concept(self, concept: str):
        """
        Add a concept node to the DAG.
        """
        self.graph.add_node(concept)

    def add_dependency(self, prerequisite: str, dependent: str):
        """
        Define a prerequisite relationship between two concepts.
        """
        self.graph.add_edge(prerequisite, dependent)

    def get_prerequisites(self, concept: str) -> List[str]:
        """
        Returns all direct prerequisites of a concept.
        """
        return list(self.graph.predecessors(concept))

    def get_dependents(self, concept: str) -> List[str]:
        """
        Returns all concepts that depend on the given concept.
        """
        return list(self.graph.successors(concept))

    def get_all_concepts(self) -> List[str]:
        """
        Returns a list of all concepts in the DAG.
        """
        return list(self.graph.nodes)

    def topological_order(self) -> List[str]:
        """
        Returns the concepts in topological order.
        """
        return list(nx.topological_sort(self.graph))

    def edges(self) -> List[Tuple[str, str]]:
        """
        Returns a list of all edges (dependencies).
        """
        return list(self.graph.edges)
