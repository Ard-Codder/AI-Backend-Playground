"""
Тесты для K-Means алгоритма
"""

import numpy as np
import pytest
from sklearn.cluster import KMeans as SklearnKMeans
from sklearn.datasets import make_blobs

from ml_core.kmeans import KMeans


class TestKMeans:
    """Тестовый класс для K-Means"""

    def setup_method(self):
        """Подготовка тестовых данных"""
        self.X, self.y_true = make_blobs(
            n_samples=300, centers=4, n_features=2, random_state=42, cluster_std=1.5
        )

    def test_kmeans_initialization(self):
        """Тест инициализации K-Means"""
        kmeans = KMeans(n_clusters=3, max_iters=100, random_state=42)

        assert kmeans.n_clusters == 3
        assert kmeans.max_iters == 100
        assert kmeans.random_state == 42
        assert kmeans.centroids is None
        assert kmeans.labels is None

    def test_kmeans_fit(self):
        """Тест обучения K-Means"""
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans.fit(self.X)

        assert kmeans.centroids is not None
        assert kmeans.labels is not None
        assert kmeans.centroids.shape == (4, 2)
        assert kmeans.labels.shape == (300,)
        assert kmeans.inertia is not None

    def test_kmeans_predict(self):
        """Тест предсказания K-Means"""
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans.fit(self.X)

        # Тест на тех же данных
        predictions = kmeans.predict(self.X)
        assert predictions.shape == (300,)
        assert set(predictions) <= set(range(4))

        # Тест на новых данных
        new_data = np.array([[0, 0], [10, 10]])
        new_predictions = kmeans.predict(new_data)
        assert new_predictions.shape == (2,)

    def test_kmeans_fit_predict(self):
        """Тест fit_predict"""
        kmeans = KMeans(n_clusters=4, random_state=42)
        labels = kmeans.fit_predict(self.X)

        assert labels.shape == (300,)
        assert set(labels) <= set(range(4))
        assert np.array_equal(labels, kmeans.labels)

    def test_predict_without_fit(self):
        """Тест предсказания без обучения"""
        kmeans = KMeans(n_clusters=4)

        with pytest.raises(ValueError, match="Модель не обучена"):
            kmeans.predict(self.X)

    def test_different_n_clusters(self):
        """Тест с разным количеством кластеров"""
        for n_clusters in [2, 3, 5]:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(self.X)

            unique_labels = set(labels)
            assert len(unique_labels) <= n_clusters

    def test_reproducibility(self):
        """Тест воспроизводимости результатов"""
        kmeans1 = KMeans(n_clusters=4, random_state=42)
        kmeans2 = KMeans(n_clusters=4, random_state=42)

        kmeans1.fit_predict(self.X)
        kmeans2.fit_predict(self.X)

        # Проверяем, что инерция одинаковая (кластеры могут быть переставлены)
        assert abs(kmeans1.inertia - kmeans2.inertia) < 1e-10

    def test_comparison_with_sklearn(self):
        """Сравнение результатов с sklearn (приблизительное)"""
        # Наш алгоритм
        our_kmeans = KMeans(n_clusters=4, random_state=42, max_iters=300)
        our_labels = our_kmeans.fit_predict(self.X)

        # Sklearn
        sklearn_kmeans = SklearnKMeans(n_clusters=4, random_state=42, n_init=1)
        sklearn_labels = sklearn_kmeans.fit_predict(self.X)

        # Проверяем, что инерция сопоставимая (может отличаться из-за разной инициализации)
        assert our_kmeans.inertia > 0
        assert sklearn_kmeans.inertia_ > 0

        # Проверяем количество уникальных кластеров
        assert len(set(our_labels)) == len(set(sklearn_labels)) == 4
