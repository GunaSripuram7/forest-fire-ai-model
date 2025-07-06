# scripts/train_fullstack.py

import os
import numpy as np
import rasterio
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Paths
stack_path = "data/processed/feature_stack.npz"
label_path = "data/processed/fire_labels/fire_20210419_downsampled_11x13.tif"
model_out  = "models/fullstack_rf.joblib"

# 1) Load feature stack
data = np.load(stack_path)["features"]  # (H, W, F)

# 2) Load labels
with rasterio.open(label_path) as src:
    labels = src.read(1)  # (H, W)

# 3) Mask valid pixels (where labels >= 0)
mask = labels >= 0

# 4) Flatten
X = data[mask]
y = labels[mask].astype(int)

print("Dataset:", X.shape, y.shape)
print("Fire pixels:", np.sum(y == 1), "Non-fire:", np.sum(y == 0))

# 5) Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 6) Train model
clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)

# 7) Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# 8) Save model
os.makedirs(os.path.dirname(model_out), exist_ok=True)
joblib.dump(clf, model_out)
print("✅ Model saved to", model_out)
