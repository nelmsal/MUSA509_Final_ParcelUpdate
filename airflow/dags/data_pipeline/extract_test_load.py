from dotenv import load_dotenv
load_dotenv()

from google.cloud import storage
import pandas as pd
import geopandas as gpd
import pathlib
import requests
import tempfile

os.chrdir(os.environ[''])

from pipeline_tools import local_file_to_gcs

bucket_name = os.environ['PIPELINE_DATA_BUCKET']
blob_name = 'test_blob'

outfile_path = r'/home/nelms/MUSA509_Final_ParcelUpdate/airflow/dags/data_pipeline/test.txt'

local_file_to_gcs(outfile_path, bucket_name, blob_name)


