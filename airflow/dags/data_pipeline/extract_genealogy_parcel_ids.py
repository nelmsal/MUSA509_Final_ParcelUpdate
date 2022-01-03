from plugins import get_arcgis_json_df


def main():
    featureservice_path = r"https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer/0/query"

    where_list = [
        "1=1", 
        #"City = 'Walnut Creek'", 
        "Current_ = 'TRUE'"
        ]
    params_dict = {
        "returnGeometry":"false",
        "outFields":"APN,Current_,Address,City",
        "geometryType":"esriGeometryPolygon"}

    final_df = get_arcgis_json_df.get_featureservice_all(featureservice_path,where_list=where_list,params_dict=params_dict)

    print(final_df)

#if __name__ == '__main__':
#    main()

main()
