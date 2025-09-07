# knowledge_model/visualization.py

"""
Visualizes the knowledge graph using matplotlib and networkx.
"""

import matplotlib.pyplot as plt
import networkx as nx


class DAGVisualizer:
    @staticmethod
    def visualize(graph: nx.DiGraph, title: str = "Knowledge DAG"):
        """
        Plots the DAG with labels.
        """
        pos = nx.spring_layout(graph, seed=42)
        plt.figure(figsize=(10, 6))
        nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='skyblue', arrows=True, arrowstyle='-|>')
        plt.title(title)
        plt.axis('off')
        plt.show()
