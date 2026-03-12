"""
Author: Subhashini G
Roll Number: 25CEM5S04

Script Name: nisar_gslc_backscatter_processing.py

Description:
This script processes NISAR Level-2 GSLC SAR data stored in HDF5 format.
It extracts HH polarization data, converts complex SAR values to
backscatter in decibels (dB), and exports the result as a GeoTIFF
using rasterio.
