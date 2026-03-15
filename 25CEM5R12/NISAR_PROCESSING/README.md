NISAR GSLC Backscatter Processing
Mission

NISAR mission (NASA–ISRO Synthetic Aperture Radar) is an Earth observation mission designed to monitor land deformation, ecosystems, and natural hazards using L-band SAR data.

This repository provides a Python workflow to convert NISAR Level-2 GSLC SAR data into GeoTIFF backscatter images that can be visualized in GIS software.

Dataset

This project uses Level-2 GSLC (Geocoded Single Look Complex) data from the NISAR mission.

The dataset contains L-band Synthetic Aperture Radar (SAR) observations acquired in descending orbit mode. The GSLC product stores complex radar measurements that can be converted into backscatter intensity (dB) for analysis and visualization.

Dataset Characteristics
| Parameter         | Description                   |
| ----------------- | ----------------------------- |
| Mission           | NISAR (NASA–ISRO SAR Mission) |
| Product Level     | Level-2 GSLC                  |
| Radar Band        | L-Band                        |
| Polarizations     | HH / HV / VH / VV             |
| Data Format       | HDF5 (.h5)                    |
| Spatial Reference | UTM (EPSG:32644)              |
| Pixel Resolution  | ~10 m × 5 m                   |
| Data Type         | Complex SAR signal            |

Data Access

The dataset can be downloaded from the Alaska Satellite Facility (ASF) Data Portal:

Features

Reads NISAR GSLC HDF5 data

Converts complex SAR signal to backscatter (dB)

Processes large scenes using block-based raster writing

Exports GeoTIFF raster files

Compatible with QGIS and other GIS software

Requirements

Install the required Python libraries before running the script.

Output

The script converts NISAR GSLC complex SAR data into a GeoTIFF backscatter raster.

Notes:

The script converts complex SAR values to decibel (dB) backscatter.

Processing is performed in 512×512 blocks to handle large NISAR scenes efficiently.

The CRS is derived from the dataset projection

![NISAR]("F:\sem2\TMHRS\NISAR_DATA\NISAR.png")
