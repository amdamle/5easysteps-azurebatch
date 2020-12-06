from __future__ import print_function
import datetime
import io
import os
import sys
import time
import config
import ffmpeg
import subprocess
from azure.storage.blob.blockblobservice import BlockBlobService

sys.path.append('.')
sys.path.append('..')

# Azure Storage Containers for reading raw files and storing converted files 
input_container_name = 'media-input'
output_container_name = 'media-output'

# function to call ffmpeg utility passing file name
def convertFiles(input_file_path):
    print("Start Conversion.....")
    output_file_path = "".join((input_file_path).split('.')[:-1]) + '.mp3'
    p = subprocess.call('ffmpeg -i {0} {1}'.format(input_file_path,output_file_path),shell=True)
    print("Conversion Completed....")
    print("File Upload to Blob ....{}".format(config.STORAGE_ACCOUNT_NAME))
    blobService = BlockBlobService(account_name=config.STORAGE_ACCOUNT_NAME,account_key=config.STORAGE_ACCOUNT_KEY)
    blobService.create_blob_from_path(output_container_name, output_file_path, output_file_path)
    print("File Upload to Blob Completed....")

if __name__ == '__main__':
    start_time = datetime.datetime.now().replace(microsecond=0)
    print('Start : {}'.format(start_time))
    print()
    filename = sys.argv[1]
    print("Processing file ---> {}".format(filename));
    convertFiles(filename)
    end_time = datetime.datetime.now().replace(microsecond=0)
    totalTime = end_time - start_time
    print("END : {}  ".format(totalTime))