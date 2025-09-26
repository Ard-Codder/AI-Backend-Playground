"""
Реализация алгоритма K-Means с нуля
"""

import argparse
from typing import Optional, Tuple

import numpy as np


class KMeans:
    """
    Реализация алгоритма K-Means кластеризации
    """

    def __init__(
        self,
        n_clusters: int = 3,
        max_iters: int = 100,
        random_state: Optional[int] = None,
    ):
        """
        Инициализация KMeans

        Args:
            n_clusters: Количество кластеров
            max_iters: Максимальное количество итераций
            random_state: Зерно случайности
        """
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.random_state = random_state
        self.centroids = None
        self.labels = None
        self.inertia = None

    def _initialize_centroids(self, X: np.ndarray) -> np.ndarray:
        """Инициализация центроидов случайным образом"""
        if self.random_state:
            np.random.seed(self.random_state)

        n_samples, n_features = X.shape
        centroids = np.zeros((self.n_clusters, n_features))

        for i in range(self.n_clusters):
            centroid = X[np.random.choice(n_samples)]
            centroids[i] = centroid

        return centroids

    def _calculate_distance(self, X: np.ndarray, centroids: np.ndarray) -> np.ndarray:
        """Вычисление евклидовых расстояний от точек до центроидов"""
        distances = np.zeros((X.shape[0], self.n_clusters))

        for idx, centroid in enumerate(centroids):
            distances[:, idx] = np.sqrt(np.sum((X - centroid) ** 2, axis=1))

        return distances

    def _assign_clusters(self, distances: np.ndarray) -> np.ndarray:
        """Назначение кластеров на основе минимальных расстояний"""
        return np.argmin(distances, axis=1)

    def _update_centroids(self, X: np.ndarray, labels: np.ndarray) -> np.ndarray:
        """Обновление центроидов"""
        centroids = np.zeros((self.n_clusters, X.shape[1]))

        for i in range(self.n_clusters):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                centroids[i] = np.mean(cluster_points, axis=0)

        return centroids

    def _calculate_inertia(
        self, X: np.ndarray, labels: np.ndarray, centroids: np.ndarray
    ) -> float:
        """Вычисление инерции (суммы квадратов расстояний до центроидов)"""
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                inertia += np.sum((cluster_points - centroids[i]) ** 2)
        return inertia

    def fit(self, X: np.ndarray) -> "KMeans":
        """
        Обучение модели K-Means

        Args:
            X: Данные для кластеризации, shape (n_samples, n_features)

        Returns:
            self: Обученная модель
        """
        # Инициализация центроидов
        self.centroids = self._initialize_centroids(X)

        for iteration in range(self.max_iters):
            # Вычисление расстояний
            distances = self._calculate_distance(X, self.centroids)

            # Назначение кластеров
            new_labels = self._assign_clusters(distances)

            # Проверка сходимости
            if iteration > 0 and np.array_equal(self.labels, new_labels):
                break

            self.labels = new_labels

            # Обновление центроидов
            self.centroids = self._update_centroids(X, self.labels)

        # Вычисление финальной инерции
        self.inertia = self._calculate_inertia(X, self.labels, self.centroids)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Предсказание кластеров для новых данных

        Args:
            X: Данные для предсказания, shape (n_samples, n_features)

        Returns:
            labels: Метки кластеров, shape (n_samples,)
        """
        if self.centroids is None:
            raise ValueError("Модель не обучена. Вызовите fit() перед predict()")

        distances = self._calculate_distance(X, self.centroids)
        return self._assign_clusters(distances)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """
        Обучение модели и предсказание кластеров

        Args:
            X: Данные для кластеризации, shape (n_samples, n_features)

        Returns:
            labels: Метки кластеров, shape (n_samples,)
        """
        self.fit(X)
        return self.labels


def main():
    """CLI интерфейс для K-Means"""
    parser = argparse.ArgumentParser(description="K-Means кластеризация")
    parser.add_argument(
        "--data", type=str, required=True, help="Путь к CSV файлу с данными"
    )
    parser.add_argument("--clusters", type=int, default=3, help="Количество кластеров")
    parser.add_argument(
        "--max-iters", type=int, default=100, help="Максимальное количество итераций"
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Зерно случайности"
    )
    parser.add_argument("--output", type=str, help="Путь для сохранения результатов")

    args = parser.parse_args()

    try:
        import pandas as pd

        # Загрузка данных
        data = pd.read_csv(args.data)
        X = data.select_dtypes(include=[np.number]).values

        print(f"Загружены данные: {X.shape}")
        print(f"Запуск K-Means с {args.clusters} кластерами...")

        # Обучение модели
        kmeans = KMeans(
            n_clusters=args.clusters,
            max_iters=args.max_iters,
            random_state=args.random_state,
        )

        labels = kmeans.fit_predict(X)

        print(f"Кластеризация завершена. Инерция: {kmeans.inertia:.2f}")

        # Сохранение результатов
        if args.output:
            result_df = data.copy()
            result_df["cluster"] = labels
            result_df.to_csv(args.output, index=False)
            print(f"Результаты сохранены в {args.output}")
        else:
            print("Результаты кластеризации:")
            for i in range(args.clusters):
                count = np.sum(labels == i)
                print(f"  Кластер {i}: {count} точек")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
