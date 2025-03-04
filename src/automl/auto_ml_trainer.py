from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_auto_ml_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy

# Example Usage
if __name__ == '__main__':
    from sklearn.datasets import load_iris
    iris = load_iris()
    model, acc = train_auto_ml_model(iris.data, iris.target)
    print(f"✔ AutoML Model Trained with Accuracy: {acc}")
