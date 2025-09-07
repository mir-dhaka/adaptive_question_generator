# bayesian_inference/learning_path.py

"""
Selects personalized learning paths based on updated mastery values.
"""

from typing import Dict, List, Tuple

class LearningPathGenerator:
    def __init__(self, mastery_threshold: float = 0.75):
        """
        :param mastery_threshold: Mastery level required to consider a concept 'learned'
        """
        self.threshold = mastery_threshold

    def generate_path(self, mastery_map: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """
        Generates a learning path based on concept mastery.

        :param mastery_map: Dict mapping concept names to mastery probabilities.
        :return: Tuple of (learned concepts, concepts to revisit)
        """
        learned = []
        to_review = []

        for concept, prob in mastery_map.items():
            if prob >= self.threshold:
                learned.append(concept)
            else:
                to_review.append(concept)

        return learned, to_review

    def recommend_next(self, to_review: List[str]) -> str:
        """
        Recommends the next concept to address.
        :param to_review: List of concepts below the mastery threshold.
        :return: The most urgent concept to work on next (e.g., first in list).
        """
        return to_review[0] if to_review else None
