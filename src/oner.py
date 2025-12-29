import pandas as pd

class OneR:
    def fit(self, X, y):
        self.best_feature = None
        self.rules = {}
        self.error = float("inf")
        self.bins = None

        for col in X.columns:
            df = pd.DataFrame({col: X[col], "y": y})

            # cria bins
            bins = pd.qcut(df[col], q=3, duplicates="drop")
            df["bin"] = bins

            # cria regra: para cada bin, a classe mais comum
            rules = df.groupby("bin", observed=False)["y"].agg(lambda x: x.value_counts().idxmax())

            # calcula erro
            preds = df["bin"].map(rules)
            error = (preds != y).mean()

            if error < self.error:
                self.error = error
                self.best_feature = col
                self.rules = rules
                self.bins = bins.cat.categories

    def predict(self, X):
        bins = pd.cut(X[self.best_feature], bins=self.bins)
        preds = bins.map(self.rules)
        preds = preds.astype("float").fillna(0).astype(int)
        return preds
