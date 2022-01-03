import geopandas as gpd
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

### download to C:\Users\nelms\Scripts\Python\Tools
### as within_which_boundary.py

def within_which_boundary(Input_gdf, bound_type='City', url='', focus_gdf='', cols=[]):
    if type(focus_gdf) == str:
        if len(url)==0:
            #if bound_type in ['Planning_Boundaries', 'Planning Boundaires', 'City']:
            #    path = r'O:\CDD\PLANNING\AN\Shapefiles\CityBoundary\AllPlanningBoundaries.shp'
            #elif bound_type in ['SP', 'Specific Plans', 'Specific_Plans', 'Specific_Plan_union']:
            #    path = r'O:\CDD\PLANNING\AN\Shapefiles\Zoning_LandUse\Specific_Plans\Specific_Plans_union.shp'
            #elif bound_type in ['FLD_ZONE','Flood_Zones', 'Flood Zones', 'Flood']:
            #    path = r'O:\CDD\PLANNING\AN\Shapefiles\Flood\Flood_Zones_union.shp'
            #elif bound_type in ['Fault Zones', 'Faults']:
            #    path = r'O:\CDD\PLANNING\GIS\Shapes\Hazards\Fault Zones Shapefiles\WC_FaultZones_Active_clean.shp'
            #elif bound_type in ['Overlays']:
            #    path = r'O:\CDD\PLANNING\AN\Shapefiles\Overlays\Overlays.shp'
            #elif bound_type in ['boxclip']:
            #    path = r'O:\CDD\PLANNING\AN\Shapefiles\CityBoundary\boxclip.shp'
            if bound_type in ['All Cities', 'Other Cities', 'Incorporation Check', 'Neighboring Cities']:
                path = f"{os.environ['HOME']}/airflow/dags/data_pipeline/static_data/Walnut_Creek_City_Boundary.parquet"
                #path = r'O:\CDD\PLANNING\GIS\Shapes\Administrative Boundaries\SF_Bay_Jurisdictions\SF_Bay_Jurisdictions_Clip.shp'
            else:
                print('Incorrect bound type input')
                raise

        else:
            path = url
            
        #Focus_gdf = gpd.read_file(path)
        Focus_gdf = gpd.read_parquet(path)
        

    else:
        Focus_gdf = focus_gdf.copy()
    
    Focus_cols = [c for c in list(Focus_gdf) if c not in ['geometry']]
    
    if len(cols)>0:
        try:
            Focus_cols = [c for c in Focus_cols if c in cols]
            if len(Focus_cols)!=len(cols):
                print('this manually inputted column is not in gdf')
                print('bad columns: ', [c for c in cols if c not in list(Focus_gdf)])
            if len(Focus_cols)==0:
                raise
        except:
            print('manualy inputted column list is not in gdf')
            print('actual columns: ', list(Focus_gdf))
    
    Input_cols = list(Input_gdf)
    if 'Within' in Input_cols:
        print('Within column was replaced')
        
    Input_index_name = Input_gdf.index.name
    if Input_index_name == None:
        Input_index_name = 'index'
        
    Input_gdf = Input_gdf.reset_index().copy()
    
    Input_pts = Input_gdf.copy()
    Input_pts['geometry'] = Input_pts['geometry'].centroid
    
    if Focus_gdf.crs != Input_pts.crs:
        Focus_gdf = Focus_gdf.to_crs(Input_pts.crs)
        print(str(Focus_gdf.crs).split(',')[0])
    
    Join_pts = gpd.sjoin(Input_pts, Focus_gdf, rsuffix='_focus')[Focus_cols]
    
    Join_gdf = Input_gdf.join(Join_pts, how='left')
    Join_gdf[Focus_cols] = Join_gdf[Focus_cols].fillna(value='')
    
    Join_gdf.set_index(Input_index_name, inplace=True)
    
    Join_gdf = Join_gdf[Input_cols+Focus_cols]

    #if bound_type == 'boxclip':
        #Join_gdf = Join_gdf.loc[Join_gdf['boxclip']=='y']
        #del Join_gdf['boxclip']

    return Join_gdf