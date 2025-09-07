# knowledge_model/student_profile.py

"""
Stores and manages student knowledge states for all concepts in the DAG.
"""

from typing import Dict


class StudentProfile:
    def __init__(self):
        self.mastery_map: Dict[str, float] = {}

    def set_mastery(self, concept: str, probability: float):
        """
        Set the mastery probability for a concept.
        """
        self.mastery_map[concept] = probability

    def get_mastery(self, concept: str) -> float:
        """
        Get the mastery level for a concept (0.0 if not set).
        """
        return self.mastery_map.get(concept, 0.0)

    def update_mastery(self, concept: str, new_probability: float):
        """
        Update the mastery level for a concept.
        """
        self.mastery_map[concept] = new_probability

    def get_all_mastery(self) -> Dict[str, float]:
        """
        Get the mastery for all concepts.
        """
        return self.mastery_map
