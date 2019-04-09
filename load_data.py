"""
Downloads sepcified required number of [random] files from Amazon S3 bucket.
Skips files that already exist.
"""

import os
from random import shuffle

import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config

from private_config import PrivateConfig

NUM_FILES_TO_LOAD = 5  # put None to download all
BUCKET_PREFIX = 'DATA/'
DATA_FOLDER = 'data/'
RANDOM = True

client = boto3.client('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
resource = boto3.resource('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
bucket = resource.Bucket(PrivateConfig.BUCKET_NAME)

# get list of all photos
def list_files(client, ls=[]):
    """List files in specific S3 URL"""
    response = client.list_objects(Bucket=PrivateConfig.BUCKET_NAME, Prefix=BUCKET_PREFIX)
    for content in response.get('Contents', []):
        ls.append(content.get('Key'))
        
    return ls

files = list_files(client)

if RANDOM:
    shuffle(files)

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

print('started')
num_downloaded = 0
for file_key in files:
    # stop downloading if we already downloaded required amount
    if NUM_FILES_TO_LOAD and num_downloaded >= NUM_FILES_TO_LOAD:
        break

    file_name = file_key.split('/')[-1]    
    file_path = DATA_FOLDER + file_name

    if os.path.isfile(file_path):
        print(f'skipping {file_name}')
        continue

    bucket.download_file(file_key, file_path)
    num_downloaded += 1
    print(f'downloaded {file_name}')
