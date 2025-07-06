# scripts/train_weather_to_fire.py

import os
import numpy as np
import rasterio
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# ✅ Paths
weather_dir = "data/processed/weather_tifs"
label_path = "data/processed/fire_labels/fire_20210419_downsampled_11x13.tif"  # <-- updated!
model_output = "models/weather_to_fire_rf.joblib"

# ✅ Load fire labels
with rasterio.open(label_path) as label_src:
    labels = label_src.read(1)
    mask = labels >= 0  # Fire: 1, No-fire: 0 → valid pixels

# ✅ Load all weather bands as stacked features
weather_features = []
weather_files = sorted([
    f for f in os.listdir(weather_dir)
    if f.endswith(".tif") and not f.endswith("_resampled.tif")
])
for file in weather_files:
    with rasterio.open(os.path.join(weather_dir, file)) as src:
        band = src.read(1)
        weather_features.append(band)

# Stack into (num_features, H, W) → transpose to (H, W, num_features)
weather_stack = np.stack(weather_features, axis=0)
weather_stack = np.transpose(weather_stack, (1, 2, 0))  # shape: (11, 13, 96)

# DEBUG: Print shape check
print("weather_stack shape:", weather_stack.shape)
print("labels shape:", labels.shape)
print("mask shape:", mask.shape)

# ✅ Extract training data
X = weather_stack[mask]           # shape: (N_pixels, 96)
y = labels[mask].astype(int)      # shape: (N_pixels,)

print(f"📊 Dataset shape: X={X.shape}, y={y.shape}")
print(f"🔥 Fire pixels: {np.sum(y == 1)}, Non-fire: {np.sum(y == 0)}")

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train model
print("🚀 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
model.fit(X_train, y_train)

# ✅ Evaluate
print("📈 Evaluation on test set:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ✅ Save model
os.makedirs(os.path.dirname(model_output), exist_ok=True)
joblib.dump(model, model_output)
print(f"✅ Model saved to: {model_output}")
