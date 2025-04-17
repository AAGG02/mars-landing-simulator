#  Mars Adaptive Landing Simulator

This project implements an intelligent landing site selection model for Mars based on terrain analysis. It simulates how an onboard system could evaluate landing safety using real elevation data and environmental constraints such as slope, soil hardness, rocks, and distance to scientific targets.

---

##  What It Does

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

##  Requirements

- Python 3.8+
- numpy
- matplotlib
- rasterio
- scipy

Install dependencies:

```bash
pip install numpy matplotlib rasterio scipy
```

---

##  Folder Structure

```
mars-landing-simulator/
│
├── mars_landing_model.py              # Main simulation script
├── data/
│   └── Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif   # DEM (not included)
```

The Mars DEM file is large and cannot be hosted here.  
You can download it from:

🔗 [USGS HRSC-MOLA Blended DEM (200 m/px)](https://astrogeology.usgs.gov/search/map/Mars/Topography/Mars_HRSC_MOLA_BlendDEM_Global_200mp)

Save it in the /data directory with the exact filename.

---

##  How to Run

After placing the DEM in the /data folder, run:

```bash
python mars_landing_model.py
```

You will see:

- Console output with:
  - Coordinates of the best landing site
  - Total safe landing area (m² and km²)

- Two visual windows:
  - 6-panel terrain analysis
  - Final highlighted safe zones and best landing point

---

##  Example Output

```
📍 Best Landing Site (x, y): (483, 526)

✅ Safe Area: 40,000,000 m² (40.00 km²)
```

---

##  Citation

If you use this project for academic purposes, please cite:

> "Adaptive Terrain-Based Landing Site Selection on Mars Using Multi-Factor Analysis", 2025.

---

##  License

This project is licensed under the MIT License.
