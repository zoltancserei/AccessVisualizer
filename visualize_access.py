'''A set of tools for visualizing Helsinki Region Travel Time Matrix data set:

find: search for files containing the user defined id
shp:create a Shapefile by joining a text file with the spatial data based on id
map:create a map of the selected id based on the selected travel mode
compare:compare travel times or travel distances between two different travel modes
'''

# Import the required modules
import os
import sys
from glob import glob
import pandas as pd
import geopandas as gpd
import mapclassify
import folium

# Read in the data
files = glob('HelsinkiTravelTimeMatrix2018/*/*')
grid_file = gpd.read_file('MetropAccess_YKR_grid/MetropAccess_YKR_grid_EurefFIN.shp')


def file_finder(YKR_ID):
    # Search for the file containing the user defined ID.
    
    found = None    
    
    for file in files:      
        if file[-11:-4] in YKR_ID:
            print(f"The id: {file[-11:-4]}, was found in file: {file}")
            found = 1
            return file
                             
    if not found:
        print(f"Could not find any file with the id: {YKR_ID}")
                
    
def make_gdf(YKR_ID):
    # Merge a csv file to the grid file.

    data = pd.read_csv(file_finder(YKR_ID), sep=';', na_values=-1)
    data = data.dropna()
    data = grid_file.merge(data, left_on='YKR_ID', right_on='from_id', how='inner')
    
    return data
    

def save_shp(YKR_ID):
    # Save the geodataframe to shapefile.
    
    gdf = make_gdf(YKR_ID)
    gdf.to_file(f"Accessibility_to_{int(gdf.to_id[0])}.shp")
    
    print('Shapefile saved to current folder.')
    
    
def static_map(YKR_ID, travel_mode):
    # Make a map based on YKR_ID and travel mode.
    
    mode = {'car': 'car_r_t', 'public': 'pt_m_tt', 'walk': 'walk_t', 'bike': 'bike_s_t'}
    
    data = make_gdf(YKR_ID)

    # Create and apply the classification
    classifier = mapclassify.NaturalBreaks.make(k=6)
    classified = data[[mode[travel_mode]]].apply(classifier)
    classified.columns = [f"{travel_mode}_classified"]
     
    data = data.join(classified)
    plot = data.plot(column=f"{travel_mode}_classified", linewidth=0)
    plot.get_figure().savefig(f"{str(YKR_ID)}_{travel_mode}.png", dpi=300)
    
    
def interactive_map(YKR_ID, travel_mode):
    # Create an interactive map 
  
    mode = {'car': 'car_r_t', 'public': 'pt_m_tt', 'walk': 'walk_t', 'bike': 'bike_s_t'}    
   
    data = make_gdf(YKR_ID)
               
    # Reproject to WGS84 (Folium requires geographic coordinates.)
    data = data.to_crs('EPSG:4326')
    
    # Create a Geo-id (Folium requires a unique identifier for each row.)
    data['geoid'] = data.index.astype(str)
    
    # Convert to geojson
    data_json = data.to_json()
        
    # Create a map instance    
    m = folium.Map(location=[60.2,24.9],
                  tiles='OpenStreetMap',
                  zoom_start=10,
                  control_scale=True)
    
    # Plot a choropleth map
    folium.Choropleth(geo_data = data_json,
                     name = 'Travel Times in 2018',
                     data = data,
                     columns=['geoid', mode[travel_mode]],
                     key_on='feature.id',
                     fill_color='YlOrRd',
                     fill_opacity=0.5,
                     line_opacity=0.2,
                     line_color='white',
                     line_weight=0,
                     highlight=False,
                     smooth_factor=1.0,
                     legend_name=f"{travel_mode.title()} travel time in minutes to {YKR_ID}"
                     ).add_to(m)
    
    outfp = f"{travel_mode.title()}_travel_time_to_{YKR_ID}.html"
    m.save(outfp)
    
    
def compare_modes(YKR_ID, comp, modes):
    # Compare two travel modes and save the result to a shapefile
    
    mode = {'time': {'car': 'car_r_t', 'public': 'pt_m_t', 'walk': 'walk_t', 'bike': 'bike_s_t'},
            'distance': {'car': 'car_r_d', 'public': 'pt_m_d', 'walk': 'walk_d', 'bike': 'bike_d'}} 
    t_m1 = mode[comp][modes[0]]
    t_m2 = mode[comp][modes[1]]

    data = make_gdf(YKR_ID)
    data['compared'] = [m1 - m2 for m1, m2 in zip(data[t_m1], data[t_m2])]
    data.to_file(f"{YKR_ID}_{modes[0]}_compared_to_{modes[1]}.shp")
    return data

def create_map(YKR_ID, travel_mode, style=None):
    # Create a statit or an interactive map based on YKR_ID and travel mode.
        
    if style == 'interactive':
        interactive_map(YKR_ID, travel_mode)
    else:
        static_map(YKR_ID, travel_mode)        


# Main function
if __name__ == '__main__':
    
    if sys.argv[1] == 'find':
        file_finder(sys.argv[2])

    elif sys.argv[1] == 'shp':
        save_shp(sys.argv[2])
    
    elif sys.argv[1] == 'map':
        create_map(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif sys.argv[1] == 'compare':
        compare_modes(sys.argv[2], sys.argv[3], modes = [sys.argv[4], sys.argv[5]])

    else:
        print('Command not found.')  