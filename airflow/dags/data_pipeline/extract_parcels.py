from typing import final


def main(ds):
    from dotenv import load_dotenv
    load_dotenv()
    import os
    from google.oauth2 import service_account
    from google.cloud import storage
    import json
    import get_arcgis_json_df as get_arcgis_json_df
    from pipeline_tools import pandas_to_gcs 

    print(os.getcwd())

    #gcs_token = os.environ#['GOOGLE_APPLICATION_CREDENTIALS']
    #print(gcs_token)
    #gcs_token = json.load(open(gcs_token))
    #gcs_token = service_account.Credentials.#from_service_account_info(gcs_token)

    gcs_bucket_name = os.environ['PIPELINE_DATA_BUCKET']
    gcs_blob_name = 'genealogy_parcels.parquet'

    old_parcel_path = r"https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer/0/query"

    parcel_ids_df = get_arcgis_json_df.get_featureservice_all(
        old_parcel_path,
        where_list = [
            "1=1", 
            #"City = 'Walnut Creek'", 
            "Current_ = 'TRUE'"],
        params_dict = {
            "returnGeometry":"false",
            "outFields":"APN,Current_,Address,City",
            "geometryType":"esriGeometryPolygon"}
        )

    old_parcel_geom_df = get_arcgis_json_df.get_featureservice_all(
        old_parcel_path,
        where_list = [
            "1=1", 
            "City = 'Walnut Creek'", 
            "Current_ = 'TRUE'"],
        params_dict = {
            "returnGeometry":"true",
            "outFields":"*",
            "geometryType":"esriGeometryPolygon",
            'f':'geojson'
            }
        )

    new_parcel_path = r'https://services2.arcgis.com/AhHMUmDoudKVXiUl/arcgis/rest/services/CCC_Assessor_Parcels_view/FeatureServer/0'
    #new_parcel_path = r'https://ccmap.cccounty.us/arcgis/rest/services/CCMAP/CCMAP/MapServer/0/query'
    #new_parcel_geom_df = get_arcgis_json_df.get_featureservice_all(
    #    new_parcel_path,
    #    where_list = [
    #        "1=1"#, 
            #"City = 'Walnut Creek'", 
            #"Current_ = 'TRUE'"
    #        ],
    #    params_dict = {
    #        "returnGeometry":"true",
    #        "outFields":"*",
    #        "geometryType":"esriGeometryPolygon",
    #        'f':'geojson'
    #        },
    #    max_record_count = 1000
    #    )

    #from get_city_boundary import within_which_boundary

    #final_df = within_which_boundary(
        #old_parcel_geom_df,
        #bound_type='All Cities')
    final_df = old_parcel_geom_df

    if 'geometry' in list(final_df):
        final_df['geometry'] = final_df['geometry'].astype(str)

    pandas_to_gcs(
        final_df, 
        gcs_bucket_name, 
        gcs_blob_name#, 
        #gcs_token
        )

if __name__ == '__main__':
    import datetime as dt
    main(ds=dt.date.today())
