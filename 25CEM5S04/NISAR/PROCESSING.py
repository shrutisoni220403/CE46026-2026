import sys
print(sys.executable)
from rasterio.crs import CRS
CRS.from_epsg(4326)
import h5py

file_path = r"C:\Users\subha\nisar\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5"

with h5py.File(file_path, "r") as f:
    def print_structure(name):
        print(name)
    f.visit(print_structure)
  import h5py

file_path = r"C:\Users\subha\nisar\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5"

with h5py.File(file_path, "r") as f:
    hh = f["science/LSAR/GSLC/grids/frequencyA/HH"]
    print("Shape:", hh.shape)
    print("Datatype:", hh.dtype)
  with h5py.File(file_path, "r") as f:
    x_coords = f["science/LSAR/GSLC/grids/frequencyA/xCoordinates"][:]
    y_coords = f["science/LSAR/GSLC/grids/frequencyA/yCoordinates"][:]
    projection = f["science/LSAR/GSLC/grids/frequencyA/projection"][()]
    x_spacing = f["science/LSAR/GSLC/grids/frequencyA/xCoordinateSpacing"][()]
    y_spacing = f["science/LSAR/GSLC/grids/frequencyA/yCoordinateSpacing"][()]

print("X spacing:", x_spacing)
print("Y spacing:", y_spacing)
print("Projection:", projection)
import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
import h5py

file_path = r"C:\Users\subha\nisar\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5"
output_path = r"HH_backscatter_dB.tif"

with h5py.File(file_path, "r") as f:
    hh = f["science/LSAR/GSLC/grids/frequencyA/HH"]
    x_coords = f["science/LSAR/GSLC/grids/frequencyA/xCoordinates"][:]
    y_coords = f["science/LSAR/GSLC/grids/frequencyA/yCoordinates"][:]
    x_spacing = f["science/LSAR/GSLC/grids/frequencyA/xCoordinateSpacing"][()]
    y_spacing = f["science/LSAR/GSLC/grids/frequencyA/yCoordinateSpacing"][()]
    projection = int(f["science/LSAR/GSLC/grids/frequencyA/projection"][()])

    rows, cols = hh.shape

    transform = from_origin(
        x_coords[0],
        y_coords[0],
        x_spacing,
        abs(y_spacing)
    )

    crs = CRS.from_epsg(projection)

    with rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        height=rows,
        width=cols,
        count=1,
        dtype="float32",
        crs=crs,
        transform=transform,
        compress="LZW"
    ) as dst:

        block_size = 1024

        for i in range(0, rows, block_size):
            row_end = min(i + block_size, rows)
            data = hh[i:row_end, :]

            power = np.abs(data) ** 2
            db = 10 * np.log10(power + 1e-10)

            dst.write(db.astype("float32"), 1, window=((i, row_end), (0, cols)))

print("Export completed!")
