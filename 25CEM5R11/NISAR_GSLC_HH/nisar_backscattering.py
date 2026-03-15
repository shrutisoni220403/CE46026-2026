pip install h5py numpy matplotlib rasterio xarray
import h5py
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import xarray as xr
file_path = r"E:\tmrh\nisar data downloaded\NISAR_L2_PR_GSLC_010_149_D_080_2005_QPDH_A_20260119T130957_20260119T131031_X05010_N_F_J_001.h5"
f = h5py.File(file_path, "r")
hh = f['science']['LSAR']['GSLC']['grids']['frequencyA']['HH']
print(hh[33400, 17000])  # Sample pixel value check

#total pixel count in hh band
total_pixels = hh.shape[0] * hh.shape[1]
print("=== HH BAND SIZE ===")
print("Rows            :", hh.shape[0])
print("Columns         :", hh.shape[1])
print("Total Pixels    :", total_pixels)
print("Total Pixels    :", f"{total_pixels:,}")  # with comma formatting

# Access X coordinates (longitude / range direction)
x_coords = f['science']['LSAR']['GSLC']['grids']['frequencyA']['xCoordinates']
print("X Coordinates shape:", x_coords.shape)
print("X Sample values:", x_coords[:5])

# Access Y coordinates (latitude / azimuth direction)
y_coords = f['science']['LSAR']['GSLC']['grids']['frequencyA']['yCoordinates']
print("Y Coordinates shape:", y_coords.shape)
print("Y Sample values:", y_coords)

# Access coordinate spacing (pixel size in meters)
x_spacing = f['science']['LSAR']['GSLC']['grids']['frequencyA']['xCoordinateSpacing']
y_spacing = f['science']['LSAR']['GSLC']['grids']['frequencyA']['yCoordinateSpacing']
print("X Spacing (m):", x_spacing[()])
print("Y Spacing (m):", y_spacing[()])

# Check projection / coordinate reference system
projection = f['science']['LSAR']['GSLC']['grids']['frequencyA']['projection']
print("Projection:", projection[()])
subset = hh[33500:34500, 17000:18000]

x_subset = x_coords[33500:34500]   # X range matching column slice
y_subset = y_coords[17000:18000]   # Y range matching row slice
print("Subset shape     :", subset.shape)
print("X range (m)      :", x_subset[0], "to", x_subset[-1])
print("Y range (m)      :", y_subset[0], "to", y_subset[-1])

magnitude = np.abs(subset)         # Get magnitude from complex values
power = magnitude ** 2             # Convert to power
power[power <= 0] = np.nan         # Avoid log(0) errors
intensity_db = 10 * np.log10(power)  # Convert to dB scale
print("Min dB:", np.nanmin(intensity_db))
print("Max dB:", np.nanmax(intensity_db))

plt.figure(figsize=(6, 6))
extent = [
    x_subset[0],    # Left   (X start)
    x_subset[-1],   # Right  (X end)
    y_subset[-1],   # Bottom (Y end)
    y_subset[0]     # Top    (Y start)
]
plt.imshow(intensity_db, cmap='gray', vmin=-30, vmax=5, extent=extent, aspect='auto')
plt.colorbar(label="Backscatter (dB)")
plt.title("NISAR L2 GSLC - HH (Subset)")
plt.xlabel("Easting (m)")           # X coordinate label
plt.ylabel("Northing (m)")          # Y coordinate label
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))  # Clean tick format
plt.tight_layout()
plt.show()
