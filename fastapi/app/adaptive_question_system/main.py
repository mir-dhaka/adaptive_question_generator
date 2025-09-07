# main.py

"""
Main entry point for the Adaptive Questioning System.
Simulates a basic run of the pipeline using synthetic student data.
"""

import networkx as nx

from knowledge_model.dag_model import create_dag
from knowledge_model.student_profile import generate_student_profile
from bayesian_inference.bayes_update import BayesianUpdater
from question_generation.adaptive_question import AdaptiveQuestionGenerator

# Step 1: Build concept DAG
concepts = {
    "Math": ["Algebra", "Geometry"],
    "Algebra": ["LinearEquations", "Quadratics"],
    "Geometry": ["Triangles", "Circles"],
    "LinearEquations": [],
    "Quadratics": [],
    "Triangles": [],
    "Circles": []
}
dag = create_dag(concepts)

# Step 2: Initialize student profile with synthetic mastery levels
profile = generate_student_profile(student_id="student_1", concept_list=list(dag.nodes))

# Step 3: Setup a synthetic question bank
question_bank = {
    concept: [f"{concept} Q{i+1}" for i in range(3)] for concept in dag.nodes
}

# Step 4: Initialize the question generator
generator = AdaptiveQuestionGenerator(dag, question_bank)

# Step 5: Generate initial adaptive questions
questions = generator.generate(student_profile=profile, num_questions=5)

# Step 6: Print generated questions
print("Generated Questions for the Student:")
for q in questions:
    print("-", q)

# Step 7: Simulate answer results and update mastery
results = {q.split()[0]: True if i % 2 == 0 else False for i, q in enumerate(questions)}
updater = BayesianUpdater(dag)
updated_profile = updater.update_mastery(profile, results)

# Step 8: Display updated profile
print("\nUpdated Student Mastery Profile:")
for concept, score in updated_profile.items():
    print(f"{concept}: {score:.2f}")
