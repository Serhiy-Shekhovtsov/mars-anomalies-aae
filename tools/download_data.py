"""
Downloads specified required number of [random] files from Amazon S3 bucket.
Skips files that already exist.
"""

import os
import argparse
import logging
from random import shuffle

import boto3
from botocore import UNSIGNED
from botocore.config import Config

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

parser = argparse.ArgumentParser(description='Downloads specified number of [random] files from Amazon S3 bucket.')

parser.add_argument('-b', '--bucket', default='', type=str,
                    help='Bucket name.')
parser.add_argument('-p', '--pref', default='DATA/', type=str,
                    help='Bucket prefix (Default: DATA/).')
parser.add_argument('-d', '--dir', default='data', type=str, metavar='PATH',
                    help='Destination path for files (Default: data).')
parser.add_argument('-n', '--nfiles', default=5, type=int, metavar='N',
                    help='Number of files to load (Default: 5). Set 0 to download all files.')
parser.add_argument('-r', '--rand', action='store_true',
                    help='Download randomly (Default: False).')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print info (Default: False).')


def main(bucket_name: str,
         bucket_pref: str,
         dest_folder: str,
         nfiles: int,
         random: bool = False,
         verbose: bool = False) -> None:

    if verbose:
        logging.getLogger().setLevel(logging.INFO)

    client = boto3.client('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
    resource = boto3.resource('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
    bucket = resource.Bucket(bucket_name)

    def list_files() -> list:
        """Lists files in specific S3 URL. Gets list of all photos.
        """
        ls = []
        response = client.list_objects(Bucket=bucket_name, Prefix=bucket_pref)

        for content in response.get('Contents', []):
            ls.append(content.get('Key'))

        return ls

    files = list_files()

    nfiles = len(files) if nfiles == 0 else nfiles

    logging.info(f'[{nfiles}] file(s) will be downloaded [{"randomly" if random else "not randomly"}] to [{dest_folder}]')

    if random:
        shuffle(files)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    logging.info('Starting...')
    num_downloaded = 0

    for file_key in files:

        # stop downloading if we already downloaded required amount
        if num_downloaded >= nfiles:
            break

        file_name = file_key.split('/')[-1]
        file_path = os.path.join(dest_folder, file_name)

        if os.path.isfile(file_path):
            logging.info(f'{file_name} file exists. Skipping...')
            continue

        logging.info(f'[{num_downloaded+1}/{nfiles}] | Downloading {file_name} ...')
        bucket.download_file(file_key, file_path)

        num_downloaded += 1
        logging.info(f'File {file_name} downloaded successfully!')

    logging.info('All files downloaded successfully!')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.bucket, args.pref, args.dir, args.nfiles, args.rand, args.verbose)
