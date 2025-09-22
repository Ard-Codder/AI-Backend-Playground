"""
ML Core - реализация алгоритмов машинного обучения с нуля
"""

__version__ = "1.0.0"
__author__ = "AI Backend Playground"

from .kmeans import KMeans
from .decision_tree import DecisionTree
from .random_forest import RandomForest

__all__ = ["KMeans", "DecisionTree", "RandomForest"]
