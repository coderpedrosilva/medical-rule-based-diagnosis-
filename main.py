from src.preprocess import load_data

X_train, X_test, y_train, y_test = load_data()

print("Sistema de Diagnóstico por Regras iniciado")
print("Amostras de treino:", len(X_train))
print("Amostras de teste:", len(X_test))
