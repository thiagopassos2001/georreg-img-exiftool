import pandas as pd
import shutil
import subprocess
import os

# Exiftool program
exiftool_path = "exiftool\exiftool.exe"

def SetCoordExiftool(file_path,lat_value,lon_value,exiftool_path="exiftool"):
    """
    Executa prompt "exiftool_path -GPSLatitude={lat_value}" -GPSLatitudeRef=S -GPSLongitude={lon_value} -GPSLongitudeRef=W file_path -P -overwrite_original
    Não retorna valor
    """

    arg_parameter = [
        exiftool_path,
        f"-GPSLatitude={lat_value}","-GPSLatitudeRef=S",
        f"-GPSLongitude={lon_value}","-GPSLongitudeRef=W",
        file_path,"-P","-overwrite_original"]
    
    subprocess.run(arg_parameter)


if __name__=="__main__":

    # Paths
    sheet_path = r"data\sheet\field_sheet.csv"
    src_img_path = r"data\src img"
    dst_img_path = r"data\dst img"

    # Sheet columns
    name_column = "FILE NAME"
    lat_column = 'LAT'
    lon_column = 'LON'

    # Sheet and available photo
    df = pd.read_csv(sheet_path,encoding="latin9")
    # Process file
    df = df.rename(columns={
        "2_7":"FILE NAME",
    })
    df[name_column] = df[name_column].apply(os.path.basename)
    df[lat_column] = df["2_1"].apply(lambda value:float(value.split(", ")[0]))
    df[lon_column] = df["2_1"].apply(lambda value:float(value.split(", ")[1]))

    # Get all files in src path
    available_files = os.listdir(src_img_path)
    # Match and filter
    df = df[df[name_column].isin(available_files)]

    # Counts
    count = 0
    max_count = len(df)

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
            # Set coords
            SetCoordExiftool(dst,lat_value,lon_value,exiftool_path=exiftool_path)
        
        except Exception as e:
            print(e)
        
        finally:
            count = count + 1
            print(f"{round(count*100/max_count,2)} %")