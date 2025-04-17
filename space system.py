from osgeo import gdal # type: ignore
import numpy as np
import matplotlib.pyplot as plt

# فتح الملف باستخدام GDAL
dem_path = r"E:\Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif"
dataset = gdal.Open(dem_path)

# الحصول على الأبعاد
cols = dataset.RasterXSize
rows = dataset.RasterYSize

# تعيين حجم جزء البيانات (نصف حجم الذاكرة)
chunk_size = 1000  # يمكنك تعديل هذه القيمة حسب الذاكرة المتاحة
n_chunks = (cols // chunk_size) + 1

# قراءة البيانات جزءًا جزءًا
terrain = np.zeros((rows, cols), dtype=np.int16)
for i in range(n_chunks):
    start_col = i * chunk_size
    end_col = min((i + 1) * chunk_size, cols)
    terrain[:, start_col:end_col] = dataset.ReadAsArray(start_col, 0, end_col - start_col, rows)

# عرض التضاريس
plt.figure(figsize=(10, 6))
plt.imshow(terrain, cmap='terrain')
plt.colorbar(label='Elevation (meters)')
plt.title("Mars Terrain from Blended DEM")
plt.show()
