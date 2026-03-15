"""
Author: Sneha Dey
Roll Number: 25CEM5R09
Program: M.Tech Geoinformatics
Institute: NIT Warangal
Course: Thermal Microwave and Hyperspectral Remote Sensing

Description:
This script reads NISAR GSLC Level-2 SAR data from an HDF5 file,
extracts HH polarization, converts complex SAR data into
backscatter intensity (sigma naught), converts it to decibel (dB),
and exports the result as a georeferenced GeoTIFF.
"""

# ------------------------------------------------
# Step 1: Import Required Libraries
# ------------------------------------------------

import numpy as np
import h5py
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS

# ------------------------------------------------
# Step 2: Input NISAR GSLC File
# ------------------------------------------------

file_path = r"C:/Users/Sneha/Downloads/NISAR_TILE/NISAR_file.h5"

# ------------------------------------------------
# Step 3: Read HH Polarization Data
# ------------------------------------------------

with h5py.File(file_path, 'r') as f:

    grid = f["science/LSAR/GSLC/grids/frequencyA"]

    hh = grid["HH"][:]

    x_coords = grid["xCoordinates"][:]
    y_coords = grid["yCoordinates"][:]

    x_spacing = grid["xCoordinateSpacing"][()]
    y_spacing = grid["yCoordinateSpacing"][()]

    projection = grid["projection"][()]

print("HH data shape:", hh.shape)

# ------------------------------------------------
# Step 4: Convert Complex SAR to Intensity
# ------------------------------------------------

intensity = np.abs(hh) ** 2

# ------------------------------------------------
# Step 5: Convert Intensity to Backscatter (dB)
# ------------------------------------------------

backscatter_db = 10 * np.log10(intensity + 1e-10)

# ------------------------------------------------
# Step 6: Handle NaN Values
# ------------------------------------------------

backscatter_db[np.isnan(backscatter_db)] = -9999

# ------------------------------------------------
# Step 7: Define GeoTransform
# ------------------------------------------------

origin_x = x_coords[0]
origin_y = y_coords[0]

transform = from_origin(
    origin_x,
    origin_y,
    x_spacing,
    abs(y_spacing)
)

crs = CRS.from_epsg(int(projection))

# ------------------------------------------------
# Step 8: Export GeoTIFF
# ------------------------------------------------

output_file = "nisar_HH_backscatter_db.tif"

with rasterio.open(
    output_file,
    "w",
    driver="GTiff",
    height=backscatter_db.shape[0],
    width=backscatter_db.shape[1],
    count=1,
    dtype="float32",
    crs=crs,
    transform=transform,
    nodata=-9999
) as dst:

    dst.write(backscatter_db.astype("float32"), 1)

print("GeoTIFF exported successfully.")