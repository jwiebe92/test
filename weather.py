from urllib.request import urlopen, Request
from urllib import request
import re
import zipfile
import os
import pandas as pd
import glob


# station_ID ist die ID der jeweiligen Stadt aus der .txt
# Stations ID ist  variabel
def weather_info(station_name: str):
    list_station_zip = []
    txt_files = []
    req = Request("ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/air_temperature/historical/")
    with urlopen(req) as response:
        content = response.read().decode('utf-8')

    # RegEx -> ((?=10minutenwerte_tu_" + station_name + ").+?(?=.zip))
    reg_ex = re.compile("(?=10minutenwerte_tu_" + station_name + ").+?(?=.zip)")
    list_station = re.findall(reg_ex, content)

    if not list_station:
        print("Station nicht vorhanden!")
    else:
        list_station_zip = list(map(lambda x: x + ".zip", list_station))
        # print(list_station_zip)

    for zip_data in list_station_zip:
        # FTP server path
        download_path = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/air_temperature" \
                        "/historical/" + zip_data + " "
        # Speichern
        request.urlretrieve(download_path, zip_data)

        # Datei mit ZipFile öffnen, extrahieren
        with zipfile.ZipFile(zip_data, 'r') as file:
            # extrahieren
            print('Extrahiere alle Dateien...')
            file.extractall()
            print('Fertig!')  # Dateien müssten im Ordner extrahiert sein
            # lese extrahierte Dateien mit Endung - .txt
            txt_files = glob.glob("*.txt")

    for txt_data in txt_files:
        # aktueller Pfad
        current_path = os.getcwd()
        # in csv umwandeln/exportieren
        df = pd.read_csv(current_path + "\\" + txt_data + "")
        print(df.shape)
        print(df.head(3))
        # df.columns = [
        #     'Stations ID , Messdatum , QN , Luftdruck in Stationshoehe der voran. 10 min , momentane Lufttemperatur in 2m Hoehe, Momentane Temperatur in 5 cm Hoehe, relative Feucht. in 2m Hoehe, Taupunkttemperatur in 2m, Taupunkttemperatur in 2m Hoehe, eor']
        print(df.head(3))
        print(df.shape)
        df.to_csv(txt_data + ".csv", sep=",", encoding='utf-8', index=False)
        df_csv = pd.read_csv(txt_data + ".csv")

        # df_csv.rename(columns=({'STATIONS_ID': 'Stations ID' , 'MESS_DATUM': 'Messdatum' , 'QN': 'QN' , 'PP_10': 'Luftdruck in Stationshoehe der voran. 10 min' , 'TT_10': 'momentane Lufttemperatur in 2m Hoehe',
        #                     'TM5_10': 'Momentane Temperatur in 5 cm Hoehe', 'RF_10': 'relative Feucht. in 2m Hoehe', 'TD_10': 'Taupunkttemperatur in 2m', 'eor': 'eor'}))
        #

        # TODO Spaltennamen ändern und MessDatum muss korrekt übergeben werden

# TODO vielleicht einfach eine Excel kreieren , Spaltennamen definieren und
#  pro Line reinschreieben (damit 1:1 das Messdatum übernommen wird)

# -> sollte "Station nicht vorhanden!" ausgeben
weather_info("00797")
# -> sollte normal durchlaufen
weather_info("00917")