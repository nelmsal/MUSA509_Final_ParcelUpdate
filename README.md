# City of Walnut Creek's Parcel Update Report
*MUSA 508 Final Project Proposal* <br>by Alexander Nelms

This pipeline seeks to utilize cloud databases & computing to transform parcel data while adding metrics on the changes, visualizations, & a map.  

## Airflow 
*missing*

## Intermediate Website
*missing.html*

## Final Public Website & Map
[City of Walnut Creek Web Page Report](https://www.walnut-creek.org/?NavID=3016)
[ArcGIS Map of Parcel Changes](https://walnutcreek.maps.arcgis.com/apps/instant/interactivelegend/index.html?appid=7065cafdba814da0a732f165b4e7f2b4)

## Presentation
[Google Slides](https://docs.google.com/presentation/d/1EzR_a2lmA9GqN19crQsbIocYkWIY_7C-idhVDaXil-k/edit?usp=sharing)

## Data Sources
1. Updated County Parcels
    * Contra Costa County Tax Assessor's ArcGIS REST Service
    * https://ccmap.cccounty.us/arcgis/rest/services/CCMAP/CCMAP/MapServer/0
      * 186 MB | 382,702+ rows | 10 columns

2. Outdated City Parcel Genealogy 
    * Walnut Creek Community & Economic Development's ArcGIS REST Service
    * https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer
    * _Now in Google Cloud Storage_ [Parquet in Bucket](https://storage.googleapis.com/staging-parcels/genealogy_parcels.parquet)

3. Walnut Creek Land Use Zoning Designations
    * Walnut Creek Community & Economic Development's ArcGIS REST Service
    * https://services2.arcgis.com/AhHMUmDoudKVXiUl/arcgis/rest/services/Zoning_Districts/FeatureServer
