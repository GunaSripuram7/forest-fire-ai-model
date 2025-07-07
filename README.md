# 🔥 Forest Fire Global Prototype – AI-Based Prediction & Spread Simulation

A prototype AI/ML pipeline for predicting and simulating **forest fire risk** and **spread** using global geospatial datasets like ERA5, MODIS, and GHSL.

---

## 🌍 Problem Statement (ISRO BAH 2025 – PS1)

Uncontrolled forest fires are influenced by weather, terrain, fuel types, and human activity. This project builds a system that:

1. **Predicts fire occurrence for the next day** (Objective 1)
2. **Simulates fire spread over time** (Objective 2)

Outputs are raster-based binary fire/no-fire maps using ML & simulation.

---

## 🧠 Objectives

### Objective 1: Fire Prediction
- Train ML model using:
  - 🔸 Weather: temperature, rainfall, humidity, wind (ERA5)
  - 🔸 Terrain: slope, elevation (SRTM DEM)
  - 🔸 Fuel: vegetation type (MODIS LC_Type1)
  - 🔸 Human: built-up stressors (GHSL)

- Output: Binary raster of fire/no-fire risk

### Objective 2: Fire Spread Simulation
- Starting from predicted fire zones, simulate how fire spreads over:
  - ⏱️ 1, 2, 3, 6, and 12 hours
- Based on:
  - 🔸 Wind vectors (u10, v10)
  - 🔸 Fuel type
  - 🔸 Slope
  - 🔸 Human presence
- Output: Sequence of fire masks or animated fire spread

---

## 📦 Project Structure

```bash
forest-fire-global-prototype/
├── data/
│   ├── raw/                # Unprocessed datasets (fire, fuel, terrain, weather, etc.)
│   └── processed/          # Resampled & aligned TIFs, stacks, masks
├── models/                 # Trained ML models
├── scripts/                # Processing & training scripts
├── outputs/                # Fire spread output GIFs or TIFs
├── notebooks/              # (Optional) Jupyter notebooks
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone & Create Virtual Environment

```bash
git clone https://github.com/GunaSripuram7/forest-fire-ai-model.git
cd forest-fire-ai-model
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```

### 2. Prepare Input Data

Download the following:

* **Fire**: MODIS/VIIRS historical fire CSVs
* **Weather**: ERA5 NetCDFs (via CDS API or Copernicus)
* **Terrain**: SRTM/DEM from Bhoonidhi or USGS
* **Fuel**: MODIS MCD12Q1 (LP DAAC)
* **Human**: GHSL built-up (JRC, 2020 or 2023)

Use provided scripts in `scripts/` to preprocess and align.

---

## 🚀 How to Run

### Step 1: Preprocessing (Optional)

```bash
python scripts/rasterize_fire_labels.py
python scripts/extract_era5_to_tif.py
python scripts/prepare_fuel_binary.py
python scripts/compute_slope_from_dem.py
```

### Step 2: Fire Spread Simulation

```bash
python scripts/fire_spread_simulation.py
```

This generates:
- `outputs/fire_spread_t_plus_1h.tif`
- ...
- `outputs/fire_spread_t_plus_12h.tif`
- `outputs/spread_comparison.png`

### Step 3: Create Fire Spread Animation

```bash
python scripts/generate_spread_gif.py
```

This generates:
- `outputs/fire_spread_animation.gif`

---

## 🧪 Model Details

| Component       | Method                           |
| --------------- | -------------------------------- |
| Fire Prediction | RandomForestClassifier (Optional) |
| Resolution      | ≈30m downsampled (11x13 grid)   |
| Fire Spread     | Cellular Automata (CA)           |
| Inputs Used     | Weather + Terrain + Fuel         |

---

## 📈 Evaluation

* **Fire Spread Simulation**: Uses directional wind alignment, fuel, and slope rules
* **Output**: Binary fire maps + side-by-side comparison plot + animation GIF

---

## 📚 Data Sources

* 🔸 **ERA5** Weather – [Copernicus CDS](https://cds.climate.copernicus.eu/)
* 🔸 **MODIS MCD12Q1** – [LP DAAC](https://lpdaac.usgs.gov/)
* 🔸 **VIIRS/MODIS Fire** – [FIRMS NASA](https://firms.modaps.eosdis.nasa.gov/)
* 🔸 **SRTM DEM** – [Bhoonidhi Portal](https://bhoonidhi.nrsc.gov.in/)
* 🔸 **GHSL Built-up** – [JRC GHSL](https://ghsl.jrc.ec.europa.eu/)

---

## 🧠 Future Work

* Replace Random Forest with UNet or LSTM (for spatial/temporal learning)
* Improve CA rules (e.g. add burn duration, fuel consumption)
* Calibrate with real-time fire evolution sequences
* Build web-based visualizer using Leaflet/Mapbox

---

## 📝 License

MIT License © 2025 Guna Sripuram

---

## 🙏 Acknowledgements

Thanks to ISRO Bhuvan, Copernicus, MODIS, and GHSL for providing open-access geospatial data that powers this AI-driven simulation framework.
