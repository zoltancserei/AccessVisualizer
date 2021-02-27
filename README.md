# AccessVisualizer

A set of tools for visualizing Helsinki Region Travel Time Matrix data set. 

More information about the datasets and the data used: https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/
The id (YKR_ID) values can be found in the attribute table of a Shapefile.

This python script uses the following libraries: os, sys, glob, pandas, geopandas, mapclassify, folium. 

The tool has four components for accessing the files, joining the attribute information with spatial data, visualizing and comparing different travel modes:

### 1. File finder:
  - search for files containing the user defined id (YKR_ID) in the input folder and it's subfolders
  - the output is a file path for further processing

### 2. Table joiner
  - create a spatial layer (Shapefile) by joining a text file with the spatial data based on id (YKR_ID)

### 3. Visualizer
- create a map of the selected id (YKR_ID) based on the selected travel mode (walking, cycling, public transport, private car)
- the map can be either static or interactive

### 4. Comparison tool
- compare travel times or travel distances between two different travel modes
- the output is a Shapefile containing the ‘compared’ column with the difference between the selected travel modes


## Usage

The script can be run from the command-line interface; the output files will be stored in the current working directory.
The script contains four command line arguments:

### 1.	find (File finder)
-	__usage__: python visualize_access.py find YKR_ID
-	__example__: python visualize_access.py find 5986740

### 2.	shp (Table joiner)
-	__usage__: python visualize_access.py shp YKR_ID
-	__example__: python visualize_access.py shp 5986740

### 3.	map (Visualizer)
-	__usage__: python visualize_access.py map YKR_ID travel_mode style
-	__example__: python visualize_access.py map 5986740 public interactive

### 4.	compare (Comparison tool)
-	__usage__: python visualize_access.py compare YKR_ID comp modes
-	__example__: python visualize_access.py compare 5986740 distance public
