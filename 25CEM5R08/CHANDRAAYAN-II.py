import spectral.io.envi as envi
import matplotlib.pyplot as plt
import numpy as np

# --- STEP A: PUT YOUR FILE PATHS HERE ---
# copy the path of your .hdr file and paste it inside the r" " below
header_file = r"C:\Users\Shruti Soni\Documents\M TECH\SEM-2\THMRS\ASSIGNMENT-2\ch2_iir_nci_20240430T2343157320_d_img_d18\data\calibrated\20240430\ch2_iir_nci_20240430T2343157320_d_img_d18.hdr"

# copy the path of your .qub file and paste it inside the r" " below
data_file = r"C:\Users\Shruti Soni\Documents\M TECH\SEM-2\THMRS\ASSIGNMENT-2\ch2_iir_nci_20240430T2343157320_d_img_d18\data\calibrated\20240430\ch2_iir_nci_20240430T2343157320_d_img_d18.qub"

# --- STEP B: LOAD THE DATA ---
print("Loading data... this might take a minute.")
try:
    # This reads the header and finds the data
    img = envi.open(header_file, data_file)

    # Load the data into a 3D array (Rows, Cols, Bands)
    data_cube = img.load()
    print(f"Success! Data shape: {data_cube.shape}")

    # --- STEP C: PLOT A PIXEL ---
    # We pick the pixel exactly in the middle of the image
    mid_row = data_cube.shape[0] // 2
    mid_col = data_cube.shape[1] // 2

    # Extract the spectral curve (all bands for this one pixel)
    spectrum = data_cube[mid_row, mid_col, :]

    # Plot it
    plt.figure(figsize=(10, 5))
    plt.plot(spectrum.flatten())
    plt.title(f'Spectral Response for Pixel ({mid_row}, {mid_col})')
    plt.xlabel('Band Number')
    plt.ylabel('Intensity')
    plt.grid(True)
    plt.show()

except Exception as e:
    print("\nERROR:")
    print(e)
    print("\nDouble check that your file paths in STEP A are correct!")
