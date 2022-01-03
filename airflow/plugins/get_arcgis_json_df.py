import requests
import sys
import pandas as pd
import json

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
        #headers=header_dict,
        params=params_dict)

    feature_size_count = json.loads(response.content.decode('utf8'))['count']

    return(feature_size_count)

def get_featureservice_df(
    rest_api_path,
    offset = 0,
    where_list = [
        "1=1", 
        "City = 'Walnut Creek'", "Current_ = 'TRUE'"],
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon"
    }):
    
    where_sql = ' AND '.join(where_list)

    params_dict['where'] = where_sql
    params_dict['resultOffset'] = offset
    params_dict['f'] = 'json'

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

        # cols = [col['name'] for col in response_json['fields']]
        extract_df = pd.DataFrame(data=[
            row['attributes'] for row in response_json['features']
            ])
        return(extract_df)
    else:
        raise

def get_featureservice_all(
    featureservice_path,
    where_list = [
        "1=1", "City = 'Walnut Creek'", "Current_ = 'TRUE'"],
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon"}
        ):
    feature_count = get_featureservice_count(
        featureservice_path,
        where_list=where_list
        )
    print(feature_count)
    max_page_size = 2000
    pages = int((feature_count/max_page_size)+1 / 1)

    featureservice_df = pd.DataFrame()

    for current_page in range(0,pages):
        current_offset_count = current_page*max_page_size

        current_page_df = get_featureservice_df(
            featureservice_path,
            offset = current_offset_count,
            where_list=where_list,
            params_dict=params_dict
            )
        
        featureservice_df = pd.concat([
            featureservice_df, current_page_df
        ])
    
    return(featureservice_df)