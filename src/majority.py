import numpy as np

class MajorityClassifier:
    def fit(self, y):
        self.majority_class = y.value_counts().idxmax()

    def predict(self, X):
        return np.full(len(X), self.majority_class)
