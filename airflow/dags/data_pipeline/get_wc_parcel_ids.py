import airflow.plugins.get_arcgis_json_df as get_arcgis_json_df

featureservice_path = r"https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer/0/query"

final_df = get_arcgis_json_df.get_featureservice_all(featureservice_path)
print(final_df)