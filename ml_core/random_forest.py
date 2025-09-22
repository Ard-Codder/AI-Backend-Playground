"""
Реализация случайного леса с нуля
"""
import numpy as np
from typing import Optional, List
import argparse
from .decision_tree import DecisionTree


class RandomForest:
    """
    Реализация случайного леса для классификации
    """
    
    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 10,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        max_features: Optional[str] = 'sqrt',
        bootstrap: bool = True,
        random_state: Optional[int] = None
    ):
        """
        Инициализация случайного леса
        
        Args:
            n_estimators: Количество деревьев в лесу
            max_depth: Максимальная глубина деревьев
            min_samples_split: Минимальное количество образцов для разделения
            min_samples_leaf: Минимальное количество образцов в листе
            max_features: Количество признаков для рассмотрения при разделении
            bootstrap: Использовать ли bootstrap выборку
            random_state: Зерно случайности
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.random_state = random_state
        self.trees: List[DecisionTree] = []
        self.feature_indices: List[np.ndarray] = []
    
    def _get_bootstrap_sample(self, X: np.ndarray, y: np.ndarray) -> tuple:
        """Создание bootstrap выборки"""
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, n_samples, replace=True)
        return X[indices], y[indices]
    
    def _get_random_features(self, n_features: int) -> np.ndarray:
        """Случайный выбор признаков"""
        if self.max_features == 'sqrt':
            n_selected = int(np.sqrt(n_features))
        elif self.max_features == 'log2':
            n_selected = int(np.log2(n_features))
        elif isinstance(self.max_features, int):
            n_selected = min(self.max_features, n_features)
        elif isinstance(self.max_features, float):
            n_selected = int(self.max_features * n_features)
        else:
            n_selected = n_features
        
        return np.random.choice(n_features, n_selected, replace=False)
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RandomForest':
        """
        Обучение случайного леса
        
        Args:
            X: Признаки, shape (n_samples, n_features)
            y: Целевые значения, shape (n_samples,)
            
        Returns:
            self: Обученная модель
        """
        if self.random_state:
            np.random.seed(self.random_state)
        
        self.trees = []
        self.feature_indices = []
        
        n_samples, n_features = X.shape
        
        for i in range(self.n_estimators):
            # Создание bootstrap выборки
            if self.bootstrap:
                X_bootstrap, y_bootstrap = self._get_bootstrap_sample(X, y)
            else:
                X_bootstrap, y_bootstrap = X, y
            
            # Случайный выбор признаков
            feature_indices = self._get_random_features(n_features)
            self.feature_indices.append(feature_indices)
            
            X_subset = X_bootstrap[:, feature_indices]
            
            # Обучение дерева
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                random_state=self.random_state + i if self.random_state else None
            )
            
            tree.fit(X_subset, y_bootstrap)
            self.trees.append(tree)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Предсказание классов
        
        Args:
            X: Признаки, shape (n_samples, n_features)
            
        Returns:
            predictions: Предсказанные классы, shape (n_samples,)
        """
        if not self.trees:
            raise ValueError("Модель не обучена. Вызовите fit() перед predict()")
        
        # Сбор предсказаний от всех деревьев
        tree_predictions = []
        
        for tree, feature_indices in zip(self.trees, self.feature_indices):
            X_subset = X[:, feature_indices]
            predictions = tree.predict(X_subset)
            tree_predictions.append(predictions)
        
        # Голосование (выбор наиболее частого класса)
        tree_predictions = np.array(tree_predictions).T
        
        final_predictions = []
        for sample_predictions in tree_predictions:
            values, counts = np.unique(sample_predictions, return_counts=True)
            final_predictions.append(values[np.argmax(counts)])
        
        return np.array(final_predictions)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Предсказание вероятностей классов
        
        Args:
            X: Признаки, shape (n_samples, n_features)
            
        Returns:
            probabilities: Вероятности классов, shape (n_samples, n_classes)
        """
        if not self.trees:
            raise ValueError("Модель не обучена. Вызовите fit() перед predict_proba()")
        
        # Сбор предсказаний от всех деревьев
        tree_predictions = []
        
        for tree, feature_indices in zip(self.trees, self.feature_indices):
            X_subset = X[:, feature_indices]
            predictions = tree.predict(X_subset)
            tree_predictions.append(predictions)
        
        tree_predictions = np.array(tree_predictions).T
        
        # Получение всех возможных классов
        all_classes = np.unique(tree_predictions)
        n_classes = len(all_classes)
        
        # Вычисление вероятностей
        probabilities = np.zeros((X.shape[0], n_classes))
        
        for i, sample_predictions in enumerate(tree_predictions):
            for j, class_label in enumerate(all_classes):
                probabilities[i, j] = np.mean(sample_predictions == class_label)
        
        return probabilities
    
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
    
    def feature_importance(self) -> np.ndarray:
        """
        Простая оценка важности признаков
        (заглушка для демонстрации)
        """
        if not self.trees:
            raise ValueError("Модель не обучена")
        
        # Упрощенная версия - равная важность для всех признаков
        n_features = len(self.feature_indices[0]) if self.feature_indices else 0
        return np.ones(n_features) / n_features


def main():
    """CLI интерфейс для случайного леса"""
    parser = argparse.ArgumentParser(description='Случайный лес для классификации')
    parser.add_argument('--data', type=str, required=True, help='Путь к CSV файлу с данными')
    parser.add_argument('--target', type=str, required=True, help='Название столбца с целевой переменной')
    parser.add_argument('--n-estimators', type=int, default=100, help='Количество деревьев')
    parser.add_argument('--max-depth', type=int, default=10, help='Максимальная глубина деревьев')
    parser.add_argument('--min-samples-split', type=int, default=2, help='Минимальное количество образцов для разделения')
    parser.add_argument('--min-samples-leaf', type=int, default=1, help='Минимальное количество образцов в листе')
    parser.add_argument('--max-features', type=str, default='sqrt', help='Количество признаков для рассмотрения')
    parser.add_argument('--test-size', type=float, default=0.2, help='Доля данных для тестирования')
    parser.add_argument('--random-state', type=int, default=42, help='Зерно случайности')
    
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
        rf = RandomForest(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            min_samples_split=args.min_samples_split,
            min_samples_leaf=args.min_samples_leaf,
            max_features=args.max_features,
            random_state=args.random_state
        )
        
        print(f"Обучение случайного леса с {args.n_estimators} деревьями...")
        rf.fit(X_train, y_train)
        
        # Оценка модели
        train_accuracy = rf.score(X_train, y_train)
        test_accuracy = rf.score(X_test, y_test)
        
        print(f"Точность на обучающей выборке: {train_accuracy:.4f}")
        print(f"Точность на тестовой выборке: {test_accuracy:.4f}")
    
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
