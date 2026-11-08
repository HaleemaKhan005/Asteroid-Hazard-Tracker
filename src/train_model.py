from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report 


base = Path(__file__).resolve().parent.parent
df = pd.read_csv(base / "data" / "asteroids.csv")
features = ["diameter_min_m", "diameter_max_m", "velocity_kmps", "miss_distance_km"]
X = df[features]
y = df["hazardous"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Training set size:", X_train.shape)
print("Test set size:", X_test.shape)
print()
print("Hazardous in training set:")
print(y_train.value_counts())
print()
print("Hazardous in test set:")
print(y_test.value_counts())

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

# Guess on the test asteroids
predictions = model.predict(X_test)
print()
print("First 10 test asteroids: actual vs predicted")
comparison = pd.DataFrame({"actual": y_test.values, "predicted": predictions})
print(comparison.head(10))
print()
print("Which features did the model rely on most?")
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print(importances)

print()
print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
print()
print("Confusion matrix (rows = actual, columns = predicted):")
print(confusion_matrix(y_test, predictions))
print()
print(classification_report(y_test, predictions))

print()
print("Effect of changing the cutoff:")
probs = model.predict_proba(X_test)[:, 1]

for cutoff in [0.5, 0.4, 0.3, 0.2, 0.1]:
    guess = probs >= cutoff
    tn, fp, fn, tp = confusion_matrix(y_test, guess).ravel()
    recall = tp / (tp + fn)
    print(f"cutoff {cutoff}: found {tp} of {tp + fn} hazardous "
          f"(recall {recall:.2f}), missed {fn}, false alarms {fp}")

    # Save the trained model for the dashboard
models_folder = base / "models"
models_folder.mkdir(exist_ok=True)
joblib.dump(model, models_folder / "asteroid_model.joblib")
print()
print("Model saved to:", models_folder / "asteroid_model.joblib")

