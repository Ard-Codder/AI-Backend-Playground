"""
Реализация дерева решений с нуля
"""

import numpy as np
from typing import Optional, Union, Dict, Any
import argparse


class Node:
    """Узел дерева решений"""

    def __init__(
        self,
        feature: Optional[int] = None,
        threshold: Optional[float] = None,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        value: Optional[Union[float, int]] = None,
    ):
        self.feature = feature  # Индекс признака для разделения
        self.threshold = threshold  # Порог для разделения
        self.left = left  # Левый потомок
        self.right = right  # Правый потомок
        self.value = value  # Значение для листового узла


class DecisionTree:
    """
    Реализация дерева решений для классификации
    """

    def __init__(
        self,
        max_depth: int = 10,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        random_state: Optional[int] = None,
    ):
        """
        Инициализация дерева решений

        Args:
            max_depth: Максимальная глубина дерева
            min_samples_split: Минимальное количество образцов для разделения
            min_samples_leaf: Минимальное количество образцов в листе
            random_state: Зерно случайности
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.root = None

    def _gini_impurity(self, y: np.ndarray) -> float:
        """Вычисление коэффициента Джини"""
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return 1 - np.sum(probabilities**2)

    def _entropy(self, y: np.ndarray) -> float:
        """Вычисление энтропии"""
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return -np.sum(probabilities * np.log2(probabilities + 1e-8))

    def _information_gain(
        self, X: np.ndarray, y: np.ndarray, feature: int, threshold: float
    ) -> float:
        """Вычисление информационного выигрыша"""
        # Разделение данных
        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask

        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return 0

        # Взвешенная энтропия после разделения
        n = len(y)
        left_entropy = self._entropy(y[left_mask])
        right_entropy = self._entropy(y[right_mask])

        weighted_entropy = (np.sum(left_mask) / n) * left_entropy + (
            np.sum(right_mask) / n
        ) * right_entropy

        # Информационный выигрыш
        return self._entropy(y) - weighted_entropy

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> tuple:
        """Поиск лучшего разделения"""
        best_gain = -1
        best_feature = None
        best_threshold = None

        n_features = X.shape[1]

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])

            for threshold in thresholds:
                gain = self._information_gain(X, y, feature, threshold)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _most_common_class(self, y: np.ndarray) -> Union[int, float]:
        """Определение наиболее частого класса"""
        values, counts = np.unique(y, return_counts=True)
        return values[np.argmax(counts)]

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """Рекурсивное построение дерева"""
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))

        # Условия остановки
        if (
            depth >= self.max_depth
            or n_classes == 1
            or n_samples < self.min_samples_split
        ):
            leaf_value = self._most_common_class(y)
            return Node(value=leaf_value)

        # Поиск лучшего разделения
        best_feature, best_threshold, best_gain = self._best_split(X, y)

        if best_gain == 0:
            leaf_value = self._most_common_class(y)
            return Node(value=leaf_value)

        # Создание разделения
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        # Проверка минимального количества образцов в листе
        if (
            np.sum(left_mask) < self.min_samples_leaf
            or np.sum(right_mask) < self.min_samples_leaf
        ):
            leaf_value = self._most_common_class(y)
            return Node(value=leaf_value)

        # Рекурсивное построение поддеревьев
        left_subtree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_subtree = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return Node(best_feature, best_threshold, left_subtree, right_subtree)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "DecisionTree":
        """
        Обучение дерева решений

        Args:
            X: Признаки, shape (n_samples, n_features)
            y: Целевые значения, shape (n_samples,)

        Returns:
            self: Обученная модель
        """
        if self.random_state:
            np.random.seed(self.random_state)

        self.root = self._build_tree(X, y)
        return self

    def _predict_sample(self, x: np.ndarray, node: Node) -> Union[int, float]:
        """Предсказание для одного образца"""
        if node.value is not None:  # Листовой узел
            return node.value

        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Предсказание классов

        Args:
            X: Признаки, shape (n_samples, n_features)

        Returns:
            predictions: Предсказанные классы, shape (n_samples,)
        """
        if self.root is None:
            raise ValueError("Модель не обучена. Вызовите fit() перед predict()")

        predictions = np.array([self._predict_sample(x, self.root) for x in X])
        return predictions

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Вычисление точности модели

        Args:
            X: Признаки, shape (n_samples, n_features)
            y: Истинные классы, shape (n_samples,)

        Returns:
            accuracy: Точность модели
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)


def main():
    """CLI интерфейс для дерева решений"""
    parser = argparse.ArgumentParser(description="Дерево решений для классификации")
    parser.add_argument(
        "--data", type=str, required=True, help="Путь к CSV файлу с данными"
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Название столбца с целевой переменной",
    )
    parser.add_argument(
        "--max-depth", type=int, default=10, help="Максимальная глубина дерева"
    )
    parser.add_argument(
        "--min-samples-split",
        type=int,
        default=2,
        help="Минимальное количество образцов для разделения",
    )
    parser.add_argument(
        "--min-samples-leaf",
        type=int,
        default=1,
        help="Минимальное количество образцов в листе",
    )
    parser.add_argument(
        "--test-size", type=float, default=0.2, help="Доля данных для тестирования"
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Зерно случайности"
    )

    args = parser.parse_args()

    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split

        # Загрузка данных
        data = pd.read_csv(args.data)
        X = data.drop(columns=[args.target]).select_dtypes(include=[np.number]).values
        y = data[args.target].values

        print(f"Загружены данные: {X.shape}")
        print(f"Целевая переменная: {len(np.unique(y))} классов")

        # Разделение на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state
        )

        print(f"Обучающая выборка: {X_train.shape}")
        print(f"Тестовая выборка: {X_test.shape}")

        # Обучение модели
        tree = DecisionTree(
            max_depth=args.max_depth,
            min_samples_split=args.min_samples_split,
            min_samples_leaf=args.min_samples_leaf,
            random_state=args.random_state,
        )

        tree.fit(X_train, y_train)

        # Оценка модели
        train_accuracy = tree.score(X_train, y_train)
        test_accuracy = tree.score(X_test, y_test)

        print(f"Точность на обучающей выборке: {train_accuracy:.4f}")
        print(f"Точность на тестовой выборке: {test_accuracy:.4f}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
