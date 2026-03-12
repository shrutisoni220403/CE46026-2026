from spectral import envi
import numpy as np
import matplotlib.pyplot as plt

# ---- paths ---- 
hdr_path = r"E:\SEM 2\TMHRS\ASSIGN 2\MOON_SPECTRAL\ch2_iir_nci_20250804T1241466686_d_img_d18.hdr"
qub_path = r"E:\SEM 2\TMHRS\ASSIGN 2\MOON_SPECTRAL\ch2_iir_nci_20250804T1241466686_d_img_d18.qub"

# 1. Open image and load data
cube = envi.open(hdr_path, image=qub_path)
data = cube.load()

# 2. Handle Scaling (Converts 1000+ values to Reflectance 0-1)
scale_factor = float(cube.metadata.get('data scale factor', 0.0001))
scaled_data = data * scale_factor

# 3. Handle Wavelengths (X-Axis)
if "wavelength" in cube.metadata:
    wavelengths = np.array(cube.metadata["wavelength"], dtype=float)
    x_label = "Wavelength ($\mu m$)"
else:
    # If metadata fails, IIRS typical range is 0.8 to 5.0 microns
    wavelengths = np.linspace(0.8, 5.0, data.shape[2])
    x_label = "Wavelength ($\mu m$) [Estimated]"

# 4. Define multiple pixels to compare (Row, Column)
pixel_list = [
    (120, 150),  # Your original pixel
    (150, 180),  # A second location
    (100, 100)   # A third location
]

# 5. Plotting with a loop
plt.figure(figsize=(10, 6))

for (r, c) in pixel_list:
    # Squeeze the 3D slice into a 1D array for each pixel
    spectrum = scaled_data[r, c, :].squeeze()
    plt.plot(wavelengths, spectrum, label=f"Pixel ({r}, {c})")

plt.title("Chandrayaan-2 IIRS: Multi-Pixel Spectral Comparison")
plt.xlabel(x_label)
plt.ylabel("Reflectance")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend() # This adds the box identifying which line is which
plt.show()
