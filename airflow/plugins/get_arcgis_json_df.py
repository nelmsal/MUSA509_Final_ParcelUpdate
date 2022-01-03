import requests
import sys
import pandas as pd
import json

# ArcGIS REST API for Feature Server Query
## 


def get_featureservice_count(
    featureservice_path = "https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer/0/query",
    where_list = [
        "1=1", "City = 'Walnut Creek'", "Current_ = 'TRUE'"]):
    params_dict = {}
    where_sql = ' AND '.join(where_list)
    params_dict['where'] = where_sql
    params_dict["returnCountOnly"] = "true"
    params_dict['f'] = 'json'

    response = requests.get(
        featureservice_path, 
        #headers=header_dict,/
        params=params_dict)

    try:
        feature_size_count = json.loads(response.content.decode('utf8'))['count']

        return(feature_size_count)
    except:
        return("Couldn't Pull File")

def get_featureservice_df(
    rest_api_path,
    offset = 0,
    where_list = [
        "1=1", 
        "City = 'Walnut Creek'", "Current_ = 'TRUE'"],
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon",
        'f':'json'
    }):
    start_dict = {}
    where_sql = ' AND '.join(where_list)

    start_dict['where'] = where_sql
    start_dict['resultOffset'] = offset
    start_dict['f'] = 'json'
    start_dict.update(params_dict)
    params_dict = start_dict

    try:
        # Retrieve data from URL
        response = requests.get(
            rest_api_path,
            params = params_dict
            )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)



    if response.status_code == 200:
        import json
        response_json = json.loads(response.content.decode('utf8'))

        import pandas as pd

        if params_dict['f'] == 'json':
            # cols = [col['name'] for col in response_json['fields']]
            extract_df = pd.DataFrame(data=[
                row['attributes'] for row in response_json['features']
                ])
        elif params_dict['f'] == 'geojson':
            from shapely.geometry import shape
            geoms = [
                        shape(row['geometry']) for row in response_json['features']
                        ]
            rows = [
                row['properties'] for row in response_json['features']
                            ]
            extract_df = pd.DataFrame(data=rows)
            extract_df['geometry'] = geoms
        return(extract_df)
    else:
        raise

def get_featureservice_json(
    rest_api_path,
    offset = 0,
    where_list = [
        "1=1", 
        "City = 'Walnut Creek'", "Current_ = 'TRUE'"],
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon",
        'f':'geojson'
    }):
    start_dict = {}
    where_sql = ' AND '.join(where_list)

    start_dict['where'] = where_sql
    start_dict['resultOffset'] = offset
    start_dict['f'] = 'json'
    start_dict.update(params_dict)
    params_dict = start_dict

    try:
        # Retrieve data from URL
        response = requests.get(
            rest_api_path,
            params = params_dict
            )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)



    if response.status_code == 200:
        import json
        response_json = json.loads(response.content.decode('utf8'))

        return(response_json)
    else:
        raise

def get_featureservice_all(
    featureservice_path,
    where_list = [
        "1=1", "City = 'Walnut Creek'", "Current_ = 'TRUE'"],
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon",
        'f':'json'
        },
    return_type = 'pandas',
    max_record_count = 2000
        ):
    feature_count = get_featureservice_count(
        featureservice_path,
        where_list=where_list
        )
    print(feature_count)
    pages = int((feature_count/max_record_count)+1 / 1)

    if return_type == 'pandas':
        featureservice = pd.DataFrame()
    if return_type == 'json':
        featureservice = {}

    for current_page in range(0,pages):
        current_offset_count = current_page*max_record_count

        if return_type == 'pandas':
            current_page_df = get_featureservice_df(
                featureservice_path,
                offset = current_offset_count,
                where_list=where_list,
                params_dict=params_dict
                )
            
            featureservice = pd.concat([
                featureservice, current_page_df
            ])
        elif return_type == 'json':
            current_page_json = get_featureservice_json(
                            featureservice_path,
                            offset = current_offset_count,
                            where_list=where_list,
                            params_dict=params_dict
                            )
            featureservice = {**current_page_json, **featureservice}
    
    return(featureservice)