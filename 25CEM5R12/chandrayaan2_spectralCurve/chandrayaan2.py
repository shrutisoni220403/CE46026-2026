import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

# =============================
# FILE PATHS
# =============================
hdr_file = r"F:\sem2\TMHRS\chandrayan2\ch2_iir_nci_20240429T1247502910_d_img_d18\data\calibrated\20240429\ch2_iir_nci_20240429T1247502910_d_img_d18.hdr"
qub_file = hdr_file.replace(".hdr", ".qub")

# OUTPUT DIRECTORY
output_dir = r"F:\sem2\TMHRS\chandrayan2\OUTPUT"
os.makedirs(output_dir, exist_ok=True)
out_file = os.path.join(output_dir, "iirs_spectral_curve.png")

print("HDR file:", hdr_file)
print("QUB file:", qub_file)

# =============================
# READ HDR
# =============================
def read_hdr(hdr_file):
    hdr = {}
    with open(hdr_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith(';'):
                k, v = line.split('=', 1)
                hdr[k.strip().lower()] = v.strip()
    return hdr

hdr = read_hdr(hdr_file)

# =============================
# LOAD QUB DATA
# =============================
samples = int(hdr['samples'])
lines   = int(hdr['lines'])
bands   = int(hdr['bands'])

data = np.fromfile(qub_file, dtype=np.float32)
cube = data.reshape((bands, lines, samples))
cube = cube.transpose(1, 2, 0)  # (rows, cols, bands)

print("Cube shape:", cube.shape)
print("Radiance min/max:", cube.min(), cube.max())

# =============================
# DEFINE WAVELENGTHS (FAIL-SAFE)
# =============================
if 'wavelengths' not in globals() or len(globals().get('wavelengths', [])) == 0:
    wavelengths = np.linspace(0.8, 5.0, cube.shape[2])

print("Wavelengths length:", len(wavelengths))  # should match cube.shape[2]

# =============================
# SPECTRAL PLOT
# =============================
pixels = [(50, 50), (100, 100), (150, 150)]

plt.figure(figsize=(10, 6))

for r, c in pixels:
    # Clip invalid negative radiance (optional)
    spectrum = cube[r, c, :]
    spectrum[spectrum < 0] = np.nan
    plt.plot(wavelengths, spectrum, label=f"Pixel ({r},{c})")

plt.xlabel("Wavelength (µm)")
plt.ylabel("Radiance")
plt.title("Chandrayaan-2 IIRS Spectral Curves")
plt.legend()
plt.grid(True)

# =============================
# SAVE PLOT
# =============================
plt.savefig(out_file, dpi=300, bbox_inches="tight")
plt.close()

#print("Plot saved as:", out_file)
#print("File exists:", os.path.exists(out_file))
#print("File size:", os.path.getsize(out_file))
