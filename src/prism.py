import pandas as pd

class Prism:
    def fit(self, X, y):
        self.rules = []
        df = X.copy()
        df["y"] = y

        for target in df["y"].unique():
            subset = df[df["y"] == target]

            while not subset.empty:
                best_attr = None
                best_value = None
                best_prob = 0

                for col in X.columns:
                    value_counts = subset[col].value_counts()

                    for val in value_counts.index:
                        prob = len(subset[subset[col] == val]) / len(df[df[col] == val])
                        if prob > best_prob:
                            best_prob = prob
                            best_attr = col
                            best_value = val

                self.rules.append((best_attr, best_value, target))
                subset = subset[subset[best_attr] != best_value]

    def predict(self, X):
        preds = []
        for _, row in X.iterrows():
            pred = 0
            for attr, val, target in self.rules:
                if row[attr] == val:
                    pred = target
            preds.append(pred)
        return preds
