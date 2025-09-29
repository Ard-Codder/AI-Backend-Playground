"""
ML Core - реализация алгоритмов машинного обучения с нуля
"""

__version__ = "1.1.0"
__author__ = "ML-Backend Playground"

from .decision_tree import DecisionTree
from .kmeans import KMeans
from .random_forest import RandomForest

__all__ = ["KMeans", "DecisionTree", "RandomForest"]
