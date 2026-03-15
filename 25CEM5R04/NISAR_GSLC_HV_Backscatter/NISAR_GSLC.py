"""
NISAR GSLC HV Backscatter Conversion to GeoTIFF
-----------------------------------------------

This script reads HV polarization data from a NISAR Level-2 GSLC product
stored in HDF5 format (.h5), converts the radar backscatter values to
decibels (dB), and exports the result as a georeferenced GeoTIFF.

Purpose
-------
• Access NISAR GSLC radar data from an HDF5 dataset
• Extract HV polarization backscatter values
• Convert radar power to decibel (dB) scale
• Preserve geospatial coordinates from the dataset
• Export the processed raster as a GeoTIFF for GIS analysis

Dataset
-------
Mission  : NISAR (NASA–ISRO Synthetic Aperture Radar)
Product  : Level-2 GSLC (Geocoded Single Look Complex)
Polarization : HV
Format   : HDF5 (.h5)

Processing Steps
----------------
1. Open the GSLC HDF5 file.
2. Extract HV polarization data and coordinate arrays.
3. Correct axis orientation if needed.
4. Convert radar amplitude to power.
5. Convert power to decibel (dB) scale.
6. Export data as a tiled and compressed GeoTIFF.

Output
------
GeoTIFF file containing HV backscatter values in decibel scale.

Author : Harshidha M
"""

import h5py
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.windows import Window


# OPEN NISAR HDF5 FILE

file = h5py.File(
    r"E:\NISAR\GSLC\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5",
    "r"
)


# ACCESS HV POLARIZATION AND COORDINATES

hv = file["/science/LSAR/GSLC/grids/frequencyB/HV"]
x = file["/science/LSAR/GSLC/grids/frequencyB/xCoordinates"]
y = file["/science/LSAR/GSLC/grids/frequencyB/yCoordinates"]

height, width = hv.shape
print("Raster size:", height, width)


# DETERMINE AXIS ORIENTATION

# Some satellite datasets store coordinates in reverse order.
# These checks ensure the raster orientation is correct.

flip_x = False
flip_y = False

if x[0] > x[-1]:
    flip_x = True

if y[0] < y[-1]:
    flip_y = True


# ---------------------------------------------------------
# DEFINE SPATIAL EXTENT
# ---------------------------------------------------------

xmin = float(min(x[0], x[-1]))
xmax = float(max(x[0], x[-1]))
ymin = float(min(y[0], y[-1]))
ymax = float(max(y[0], y[-1]))

transform = from_bounds(xmin, ymin, xmax, ymax, width, height)


# WRITE OUTPUT GEOTIFF (BLOCK PROCESSING)
# Large SAR datasets may not fit into memory.
# Therefore the raster is processed in 512x512 blocks.

with rasterio.open(
    "nisar_hv_backscatter.tif",
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype="float32",
    crs="EPSG:32643",  # UTM Zone 43N
    transform=transform,
    tiled=True,
    blockxsize=512,
    blockysize=512,
    compress="lzw"
) as dst:

    for i in range(0, height, 512):
        for j in range(0, width, 512):

            row_end = min(i + 512, height)
            col_end = min(j + 512, width)

            # Read small chunk of the SAR image
            chunk = hv[i:row_end, j:col_end]

            # Apply orientation correction if required
            if flip_x:
                chunk = np.fliplr(chunk)
            if flip_y:
                chunk = np.flipud(chunk)

            # CONVERT BACKSCATTER TO DECIBEL SCALE

            power = np.abs(chunk) ** 2
            power[power == 0] = np.nan

            db = 10 * np.log10(power)

            # Limit dynamic range for visualization
            db = np.clip(db, -30, 10).astype("float32")

            window = Window(
                col_off=j,
                row_off=i,
                width=col_end - j,
                height=row_end - i
            )

            dst.write(db, 1, window=window)


print("GeoTIFF exported successfully.")

file.close()
