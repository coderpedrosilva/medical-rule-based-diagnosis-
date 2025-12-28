from src.preprocess import load_data
from src.majority import MajorityClassifier

X_train, X_test, y_train, y_test = load_data()

model = MajorityClassifier()
model.fit(y_train)
predictions = model.predict(X_test)

print("Majority prediction:", predictions[:10])
