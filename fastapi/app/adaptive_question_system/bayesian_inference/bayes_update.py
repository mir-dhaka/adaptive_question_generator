# bayesian_inference/bayes_update.py

"""
Implements Bayesian Knowledge Tracing (BKT) for updating student mastery levels.
"""

import numpy as np

class BayesianUpdater:
    def __init__(self, initial_mastery=0.5, p_learn=0.2, p_slip=0.1, p_guess=0.2):
        """
        Initializes parameters for Bayesian update.

        :param initial_mastery: Prior probability of student knowing the skill.
        :param p_learn: Probability of learning the skill after an attempt.
        :param p_slip: Probability of a student knowing but giving a wrong answer.
        :param p_guess: Probability of a student not knowing but giving a correct answer.
        """
        self.mastery = initial_mastery
        self.p_learn = p_learn
        self.p_slip = p_slip
        self.p_guess = p_guess

    def update(self, correct: bool) -> float:
        """
        Update the mastery level based on the correctness of the response.

        :param correct: Boolean indicating if the student answered correctly.
        :return: Updated mastery probability.
        """
        p_mastery = self.mastery

        if correct:
            numerator = p_mastery * (1 - self.p_slip)
            denominator = numerator + (1 - p_mastery) * self.p_guess
        else:
            numerator = p_mastery * self.p_slip
            denominator = numerator + (1 - p_mastery) * (1 - self.p_guess)

        posterior = numerator / denominator if denominator > 0 else p_mastery
        updated_mastery = posterior + (1 - posterior) * self.p_learn
        self.mastery = updated_mastery
        return self.mastery

    def get_mastery(self) -> float:
        """
        Returns the current mastery level.
        """
        return self.mastery
