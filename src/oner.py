import pandas as pd

class OneR:
    def fit(self, X, y):
        self.best_feature = None
        self.rules = {}
        self.error = float("inf")

        for col in X.columns:
            df = pd.DataFrame({col: X[col], "y": y})

            # cria bins
            df["bin"] = pd.qcut(df[col], q=3, duplicates="drop")

            # cria regra: para cada bin, a classe mais comum
            rules = df.groupby("bin", observed=False)["y"].agg(lambda x: x.value_counts().idxmax())

            # calcula erro
            preds = df["bin"].map(rules)
            error = (preds != y).mean()

            if error < self.error:
                self.error = error
                self.best_feature = col
                self.rules = rules

    def predict(self, X):
        bins = pd.qcut(X[self.best_feature], q=3, duplicates="drop")
        return bins.map(self.rules).fillna(0).astype(int)
