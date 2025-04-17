import numpy as np
import matplotlib.pyplot as plt
import rasterio
from scipy.ndimage import distance_transform_edt
import matplotlib.gridspec as gridspec

# === Load DEM ===
def load_dem(filepath, window_size=1000):
    with rasterio.open(filepath) as dataset:
        window = rasterio.windows.Window(0, 0, window_size, window_size)
        elevation_data = dataset.read(1, window=window)
        return elevation_data

# === Compute slope map ===
def compute_slope(elevation_data, pixel_size=200):
    dzdx = np.gradient(elevation_data, axis=1) / pixel_size
    dzdy = np.gradient(elevation_data, axis=0) / pixel_size
    slope = np.sqrt(dzdx**2 + dzdy**2)
    slope_deg = np.rad2deg(np.arctan(slope))
    return slope_deg

# === Create binary hazard map based on slope threshold ===
def classify_risk(slope_deg, slope_threshold=15):
    classification = np.zeros_like(slope_deg, dtype=np.uint8)
    classification[slope_deg > slope_threshold] = 1
    return classification

# === Generate random soil hardness map ===
def generate_soil_hardness(shape):
    return np.clip(np.random.normal(loc=0.7, scale=0.2, size=shape), 0, 1)

# === Generate random rock obstacle map ===
def generate_rock_obstacles(shape, num_rocks=80):
    rock_map = np.zeros(shape, dtype=np.uint8)
    for _ in range(num_rocks):
        y = np.random.randint(5, shape[0] - 5)
        x = np.random.randint(5, shape[1] - 5)
        rock_map[y - 2:y + 3, x - 2:x + 3] = 1
    return rock_map

# === Compute distance from a scientific target point ===
def compute_distance_map(shape, target_point):
    target_map = np.zeros(shape, dtype=np.uint8)
    target_map[target_point[1], target_point[0]] = 1
    return distance_transform_edt(1 - target_map)

# === Normalize a matrix to [0, 1] ===
def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-8)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    dem = load_dem("data/Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif")
    slope = compute_slope(dem)
    shape = dem.shape

    soil_hardness = generate_soil_hardness(shape)
    rock_map = generate_rock_obstacles(shape)
    target_point = (shape[1] // 2, shape[0] // 2)
    distance_map = compute_distance_map(shape, target_point)

    # Normalized and inverted scores where needed
    rock_score = 1 - rock_map
    slope_score = 1 - normalize(slope)
    soil_score = normalize(soil_hardness)
    dist_score = 1 - normalize(distance_map)

    # Weighted sum for terrain suitability
    w_slope, w_soil, w_rock, w_dist = 0.4, 0.3, 0.2, 0.1
    suitability = (
        w_slope * slope_score +
        w_soil * soil_score +
        w_rock * rock_score +
        w_dist * dist_score
    )

    # Create binary mask for good zones
    landing_zones = suitability > 0.8

    # Find the best point within valid zones
    if np.sum(landing_zones) > 0:
        best_index = np.unravel_index(np.argmax(suitability * landing_zones), suitability.shape)
        print(f"\n📍 Best Landing Site (x, y): {best_index[::-1]}")
    else:
        best_index = None
        print("❌ No suitable landing zone found.")

    # Safe area calculation
    safe_pixel_count = np.sum(landing_zones)
    pixel_area_m2 = 200 * 200
    total_area_m2 = safe_pixel_count * pixel_area_m2
    total_area_km2 = total_area_m2 / 1e6
    print(f"\n✅ Safe Area: {total_area_m2:,.0f} m² ({total_area_km2:.2f} km²)")

    # === Professional plot with explanations ===
    fig = plt.figure(figsize=(22, 12))
    gs = gridspec.GridSpec(2, 3, figure=fig)
    titles = [
        "1. Elevation (DEM)",
        "2. Slope (degrees)",
        "3. Soil Hardness",
        "4. Obstacle Map",
        "5. Proximity to Target",
        "6. Final Landing Zones"
    ]
    descriptions = [
        "Topographic height at each point on Mars surface",
        "Surface inclination angle (higher = more dangerous)",
        "Simulated surface hardness (1 = hardest, 0 = soft)",
        "Locations of rocks or surface obstacles",
        "Closer points to scientific target are more favorable",
        "Safe regions that meet all criteria above 80%"
    ]
    data = [dem, slope, soil_hardness, rock_map, dist_score, landing_zones]
    cmaps = ['terrain', 'inferno', 'YlGn', 'gray', 'Blues', 'Greens']

    for idx in range(6):
        ax = fig.add_subplot(gs[idx])
        im = ax.imshow(data[idx], cmap=cmaps[idx])
        ax.set_title(titles[idx], fontsize=14, weight='bold')
        ax.text(0.5, -0.12, descriptions[idx],
                ha='center', va='center', transform=ax.transAxes, fontsize=10, color='dimgray')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("Mars Adaptive Landing Analysis – Terrain Evaluation & Suitability Map",
                 fontsize=18, weight='bold', color='navy')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # === Final highlight map ===
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ax2.imshow(dem, cmap='terrain')
    safe_y, safe_x = np.where(landing_zones == 1)
    ax2.scatter(safe_x, safe_y, color='cyan', s=5, label="Safe Zones", alpha=0.6)

    if best_index:
        ax2.plot(best_index[1], best_index[0], 'bo', markersize=10, label="Best Landing Site")

    ax2.set_title("Landing Zones Highlighted (DEM + Safe Points)")
    ax2.legend(loc='lower right')
    ax2.axis("off")
    plt.tight_layout()
    plt.show()

