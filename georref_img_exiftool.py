# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:21:27 2024

@author: thiagop
"""

import pandas as pd
import shutil
import subprocess
import os

# Exiftool program
exiftool_path = "exiftool\exiftool.exe"

# Paths
sheet_path = r"C:\Users\thiagop\Desktop\SINV_Placas_Crateus.xlsx"
src_img_path = r'C:\Users\thiagop\Desktop\1_BLOCO_Images\1_BLOCO_Images'
dst_img_path = r'C:\Users\thiagop\Desktop\Registro Fotográfico Georreferenciado'

# Sheet columns
name_column = "FILE NAME"
lat_column = 'LAT'
lon_column = 'LON'

# Sheet and available photo
df = pd.read_excel(sheet_path)
available_files = os.listdir(src_img_path)

# Match and filter
df = df[df[name_column].isin(available_files)]

# Count
count = 0
max_count = len(df)

print(df)

for index, row in df.iterrows():
    try:
        # Lat and lon value
        lat_value = abs(row[lat_column])
        lon_value = abs(row[lon_column])

        # Join paths
        file_name = row[name_column]
        src = os.path.join(src_img_path,file_name)
        dst = os.path.join(dst_img_path,file_name)

        # Copy file
        shutil.copyfile(src,dst)

        # Args
        arg_parameter = [
            exiftool_path,
            f"-GPSLatitude={lat_value}",
            "-GPSLatitudeRef=S",
            f"-GPSLongitude={lon_value}",
            "-GPSLongitudeRef=W",
            dst,
            "-P",
            "-overwrite_original"
            ]
        
        # Run
        subprocess.run(arg_parameter)
    
    except Exception as e:
        print(e)
    
    finally:
        count = count + 1
        print(f"{round(count*100/max_count,2)} %")
    


