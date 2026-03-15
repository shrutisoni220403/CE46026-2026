# Author: Sneha Dey
# Roll Number: 25CEM5R09
# Course: Thermal Microwave and Hyperspectral Remote Sensing
# Institute: NIT Warangal

# Description:
# This script generates Chandrayaan-II Spectral curve


import numpy as np
import matplotlib.pyplot as plt

hdr_file = "C:\Users\Sneha\Downloads\ch2_iir_nci_20200206T0345441415_d_img_d18\data\calibrated\20200206\ch2_iir_nci_20200206T0345441415_d_img_d18.hdr"
qub_file = "C:\Users\Sneha\Downloads\ch2_iir_nci_20200206T0345441415_d_img_d18\data\calibrated\20200206\ch2_iir_nci_20200206T0345441415_d_img_d18.qub"

hdr = {}
f = open(hdr_file, "r")
for line in f:
    if "=" in line:
        key, value = line.split("=")
        hdr[key.strip().lower()] = value.strip()
f.close()

samples = int(hdr["samples"])
lines = int(hdr["lines"])
bands = int(hdr["bands"])
data_type = int(hdr["data type"])
interleave = hdr["interleave"].lower()

if data_type == 4:
    dtype = np.float32
elif data_type == 2:
    dtype = np.int16
else:
    dtype = np.float32

data = np.fromfile(qub_file, dtype=dtype)

if interleave == "bsq":
    cube = data.reshape(bands, lines, samples)
elif interleave == "bil":
    cube = data.reshape(lines, bands, samples)
    cube = cube.transpose(1, 0, 2)
elif interleave == "bip":
    cube = data.reshape(lines, samples, bands)
    cube = cube.transpose(2, 0, 1)

print(cube.shape)

row = 100
col = 100

spectrum = cube[:, row, col]

plt.plot(spectrum)
plt.xlabel("Band Number")
plt.ylabel("Reflectance")
plt.title("Spectral Response of One Pixel")
plt.show()

rows = [50, 100, 150]
cols = [50, 100, 150]

for i in range(3):
    plt.plot(cube[:, rows[i], cols[i]])

plt.xlabel("Band Number")
plt.ylabel("Reflectance")
plt.title("Spectral Response of Multiple Pixels")
plt.show()

