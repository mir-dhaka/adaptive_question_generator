# question_generation/adaptive_question.py

"""
Generates adaptive questions based on student profile and concept DAG.
"""

from typing import Dict, List
import random
import networkx as nx


class AdaptiveQuestionGenerator:
    def __init__(self, concept_graph: nx.DiGraph, question_bank: Dict[str, List[str]]):
        """
        :param concept_graph: Directed graph of concepts (prerequisite DAG).
        :param question_bank: Dictionary mapping concept to list of questions.
        """
        self.graph = concept_graph
        self.question_bank = question_bank

    def _get_weak_concepts(self, profile: Dict[str, float], threshold: float = 0.6) -> List[str]:
        """
        Return list of concepts with mastery below the threshold.
        """
        return [concept for concept, score in profile.items() if score < threshold]

    def generate(self, student_profile: Dict[str, float], num_questions: int = 5) -> List[str]:
        """
        Generate a list of adaptive questions based on weakest concepts.
        """
        weak_concepts = self._get_weak_concepts(student_profile)
        questions = []

        for concept in weak_concepts:
            if concept in self.question_bank:
                qlist = self.question_bank[concept]
                if qlist:
                    sampled = random.sample(qlist, min(len(qlist), num_questions - len(questions)))
                    questions.extend(sampled)
            if len(questions) >= num_questions:
                break

        # Fallback: fill remaining with random questions
        if len(questions) < num_questions:
            all_questions = [q for qs in self.question_bank.values() for q in qs]
            random.shuffle(all_questions)
            questions += all_questions[:num_questions - len(questions)]

        return questions
