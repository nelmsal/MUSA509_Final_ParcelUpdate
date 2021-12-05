# City of Walnut Creek's Parcel Update Report
*MUSA 508 Final Project Proposal*<br>by Alexander Nelms

## Abstract
The City of Walnut Creek, like many cities, uses parcel data as a method of organizing the land, permitting, and policy decisions. However, the [county’s tax assessor’s office](https://www.contracosta.ca.gov/191/Assessor) organizes the parcel’s assessors parcel number (APN), owners, address, geographic shape, and various characteristic data. The larger issue is that Walnut Creek and many medium-to-small cities (< 100k people) have not developed the data infrastructure to seamlessly:
1. <ins>Extract</ins> the updated parcel data from the county,
2. <ins>Transform</ins> the parcels to the context of the city and individual departments (e.g. determine parcel changes, attach local land use designations), *and*
3. <ins>Load</ins> the transformed data into databases, software, and reports. 

Most of these cities' single GIS Analyst has to waste hours of their time by manually processing this ETL pipeline. One typically lost process is determining the parcel changes (a.k.a. Genealogy) as it requires additional manually analysis. This pipeline seeks to utilize cloud databases & computing to transform parcel data while adding metrics on the changes, visualizations, & a map.  

## Data Sources

1. Updated County Parcels
  * Contra Costa County Tax Assessor's ArcGIS REST Service
    * https://ccmap.cccounty.us/arcgis/rest/services/CCMAP/CCMAP/MapServer/0
    * 186 MB | 382,702+ rows | 10 columns

2. Outdated City Parcel Genealogy 
  * Walnut Creek Community & Economic Development's ArcGIS REST Service
  * https://services2.arcgis.com/AhHMUmDoudKVXiUl/ArcGIS/rest/services/Master_Parcels/FeatureServer

3. Walnut Creek Land Use Zoning Designations
  * Walnut Creek Community & Economic Development's ArcGIS REST Service
  * https://services2.arcgis.com/AhHMUmDoudKVXiUl/arcgis/rest/services/Zoning_Districts/FeatureServer

## Wireframe

