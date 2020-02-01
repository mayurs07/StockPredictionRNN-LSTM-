# -*- coding: utf-8 -*-

import datetime
import os
import requests
import zipfile

# URL generator

def generate_URL(dateFrom,dateTo=datetime.date.today(),td=datetime.timedelta(days=1)):

    endpoint = "https://www1.nseindia.com/content/historical/EQUITIES"

    while dateFrom <= dateTo:
        year = dateFrom.year
        month = dateFrom.strftime('%b').upper()
        filename_part = dateFrom.strftime('%d%b%Y').upper()

        yield f"{endpoint}/{year}/{month}/cm{filename_part}bhav.csv.zip"
        dateFrom += td


#  file download
        
def download_file(fileURL,outputFile=None,targetDir=None):

    targetDir = targetDir if targetDir else os.getcwd()
    outputFile = outputFile if outputFile else fileURL.split('/')[-1]
    
    response = requests.get(fileURL, stream = True)

    if response.status_code == 200:
        outputFile = os.path.join(targetDir,outputFile)
        with open(outputFile,"wb") as fd: 
            for chunk in response.iter_content(chunk_size=1024): 
             # writing one chunk at a time to output file 
             if chunk: 
                 fd.write(chunk)
        print(f"{os.path.split(outputFile)[-1]} downloaded.")
    else:
        print(f"Error: {response.status_code} {outputFile} {response.reason}")

def main():
    for i in range(1,365):
        d = datetime.date.today()-datetime.timedelta(days=i)
        print("Downloading Data ...")
        for t in generate_URL(d):
            download_file(t)
   


if __name__ == '__main__':
    main()
