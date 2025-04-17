# mars-landing-simulator
Adaptive terrain-based landing site selection system for Mars using DEM analysis

# 🚀 Mars Adaptive Landing Simulator

This project implements an intelligent landing site selection model for Mars based on terrain analysis. It simulates how an onboard system could evaluate landing safety using real elevation data and environmental constraints such as slope, soil hardness, rocks, and distance to scientific targets.

---

## 🧠 What It Does

- Loads real Mars elevation data (HRSC + MOLA DEM)
- Computes slope angle to detect hazardous terrain
- Simulates soil hardness variability
- Generates synthetic obstacle maps (rocks)
- Evaluates proximity to a scientific target
- Combines all factors into a normalized suitability score
- Highlights safe landing zones (score > 0.8)
- Automatically selects the best landing site
- Visualizes the full terrain analysis in a professional layout

---

## 🛠 Requirements

- Python 3.8+
- numpy
- matplotlib
- rasterio
- scipy

Install dependencies:

```bash
pip install numpy matplotlib rasterio scipy
