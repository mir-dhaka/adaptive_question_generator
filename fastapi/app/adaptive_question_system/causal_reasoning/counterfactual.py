# causal_reasoning/counterfactual.py

"""
Simple counterfactual reasoning based on student profiles and concept mastery.
"""

from typing import Dict


class CounterfactualAnalyzer:
    def __init__(self, student_profile: Dict[str, float]):
        self.profile = student_profile

    def ask_counterfactual(self, concept: str, desired_mastery: float) -> str:
        """
        Provides a counterfactual suggestion for improving mastery.
        """
        current = self.profile.get(concept, 0.0)
        if current >= desired_mastery:
            return f"No need for counterfactual. Current mastery ({current}) >= desired ({desired_mastery})"
        
        # Suggest increasing related concept mastery (simplified)
        suggestion = f"To improve mastery in '{concept}' from {current} to {desired_mastery}, review its prerequisites or related weak concepts."
        return suggestion
