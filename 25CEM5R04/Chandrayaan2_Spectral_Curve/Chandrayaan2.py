"""
Chandrayaan-2 IIRS Spectral Analysis
------------------------------------

This script reads hyperspectral data from the Chandrayaan-2 IIRS sensor
stored in ENVI format (.hdr + .qub files) and visualizes spectral
radiance values for selected pixels.

Purpose
-------
• Load hyperspectral cube data from Chandrayaan-2 IIRS dataset
• Extract spectral information for specific pixel locations
• Plot spectral curves to analyse radiance variation across bands

Dataset
-------
Sensor : Chandrayaan-2 IIRS (Imaging Infrared Spectrometer)
Format : ENVI header (.hdr) + binary cube (.qub)

Output
------
A spectral curve plot showing radiance variation across spectral bands
for selected pixels in the image.

Author : Harshidha M
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# HDR FILE PATH
hdr_file = r"D:\2 SEM PG Geoinfo\TMHRS\Chandraayan - 2\ch2_iir_nci_20250807T1513117694_d_img_d18\data\calibrated\20250807\ch2_iir_nci_20250807T1513117694_d_img_d18.hdr"
print("HDR file:", hdr_file)


# FUNCTION: READ HDR FILE
def read_hdr(hdr_file):
    """
    Reads ENVI header (.hdr) file and extracts metadata.

    Parameters
    ----------
    hdr_file : str
        Path to HDR file

    Returns
    -------
    dict
        Dictionary containing header metadata
    """

    header = {}

    with open(hdr_file, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                header[key.strip().lower()] = value.strip()

    return header


hdr = read_hdr(hdr_file)


# PRINT HDR CONTENTS
print("\n--- HDR CONTENTS ---")
for k, v in hdr.items():
    print(k, ":", v)


# FUNCTION: LOAD QUB FILE
def load_qub(qub_file, hdr):
    """
    Loads hyperspectral cube from .qub binary file.

    Parameters
    ----------
    qub_file : str
        Path to QUB file
    hdr : dict
        Header metadata

    Returns
    -------
    numpy.ndarray
        Hyperspectral data cube with shape (rows, cols, bands)
    """

    samples = int(hdr['samples'])
    lines = int(hdr['lines'])
    bands = int(hdr['bands'])
    data_type = int(hdr['data type'])

    envi_dtype = {
        1: np.uint8,
        2: np.int16,
        3: np.int32,
        4: np.float32,
        5: np.float64,
        12: np.uint16
    }

    dtype = envi_dtype[data_type]

    data = np.fromfile(qub_file, dtype=dtype)

    cube = data.reshape((bands, lines, samples))

    # Convert to (rows, cols, bands)
    cube = np.transpose(cube, (1, 2, 0))

    return cube


# QUB FILE PATH
qub_file = r"D:\2 SEM PG Geoinfo\TMHRS\Chandraayan - 2\ch2_iir_nci_20250807T1513117694_d_img_d18\data\calibrated\20250807\ch2_iir_nci_20250807T1513117694_d_img_d18.qub"

cube = load_qub(qub_file, hdr)

print("\nCube shape:", cube.shape)


# EXTRACT WAVELENGTHS IF AVAILABLE

if 'wavelength' in hdr:

    wavelengths = np.array(
        [float(w) for w in hdr['wavelength']
         .replace('{', '')
         .replace('}', '')
         .split(',')]
    )

    x_axis = wavelengths
    x_label = "Wavelength (µm)"

else:

    # If wavelength metadata is unavailable
    x_axis = np.arange(cube.shape[2])
    x_label = "Spectral Band Index"

print("Number of spectral bands:", len(x_axis))



# PIXELS TO ANALYSE
pixels = [(50, 50), (100, 100), (150, 150)]


# SPECTRAL PLOTS
plt.figure(figsize=(10, 6))

for (r, c) in pixels:

    if r < cube.shape[0] and c < cube.shape[1]:
        plt.plot(x_axis, cube[r, c, :], label=f"Pixel ({r},{c})")

    else:
        print(f"Pixel ({r},{c}) is outside image bounds")


plt.xlabel(x_label)
plt.ylabel("Radiance / Reflectance")

plt.title("Chandrayaan-2 IIRS Spectral Curves")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.show()
