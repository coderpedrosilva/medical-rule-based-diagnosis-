import pandas as pd
from sklearn.model_selection import train_test_split

def load_data():
    df = pd.read_csv("data/diabetes.csv")

    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    return train_test_split(X, y, test_size=0.3, random_state=42)
