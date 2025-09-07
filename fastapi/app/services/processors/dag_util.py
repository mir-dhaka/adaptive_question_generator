import os
import networkx as nx

import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server-side image generation
import matplotlib.pyplot as plt

from sqlalchemy.orm import Session
from app.models.dag_models import DAG, KC, DAGEdge

class DagUtil:
    @staticmethod
    def generate_dag_image(db: Session, dag_id: int, save_dir: str = "static/files") -> str:
        """
        Generates a DAG image using only networkx + matplotlib (no pygraphviz/pydot),
        saves it internally, and returns only the filename.
        """
        os.makedirs(save_dir, exist_ok=True)

        # Fetch DAG
        dag_obj = db.query(DAG).filter(DAG.id == dag_id).first()
        if not dag_obj:
            raise ValueError(f"DAG with id {dag_id} not found")

        # Fetch edges
        edges = db.query(DAGEdge).filter(DAGEdge.dag_id == dag_id).all()
        if not edges:
            raise ValueError(f"No edges found for DAG id {dag_id}")
        
        # Fetch all KCs to map id -> title
        kcs = db.query(KC).all()
        kc_map = {kc.id: kc.title for kc in kcs}

        # Build NetworkX DAG
        G = nx.DiGraph()
        for edge in edges:
            from_title = kc_map.get(edge.from_kc_id, str(edge.from_kc_id))
            to_title = kc_map.get(edge.to_kc_id, str(edge.to_kc_id))
            G.add_edge(from_title, to_title)

        # Simple layout (no pygraphviz)
        pos = nx.spring_layout(G, seed=42)  # seed for consistent layout

        # Plot
        plt.figure(figsize=(12, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            arrows=True,
            node_size=2000,
            node_color="skyblue",
            font_size=12,
            font_weight="bold",
            arrowsize=20
        )

        # Save internally
        filename = f"dag_{dag_id}.png"
        filepath = os.path.join(save_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()

        return filename  # only filename returned
