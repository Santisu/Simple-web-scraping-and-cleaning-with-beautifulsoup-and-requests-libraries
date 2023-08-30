import csv
import os

# Select the csv file's path
ruta_script = os.path.dirname(os.path.abspath(__file__))
registro_csv = os.path.join(ruta_script, 'one_piece_manga.csv')
# Declare a dict that will contain the inconsistent data
dict_string = {}


# We open the file and through a for loop we are going to check that every date element is digit,
# if it isn't, the inconsistent dates with the row number and the data will be stored in the dict
with open(registro_csv, mode='r', newline='', encoding='utf-8') as archivo:
    reader = csv.reader(archivo)
    for registro, linea in enumerate(reader, start=1):
        if linea:
            fecha = linea[-1] 
            print(f"Línea {registro}: {fecha}")
            fecha_list = fecha.split('-')
            for element in fecha_list:
                element = element.strip(' ')
                if not element.isdigit():
                    dict_string[registro] = fecha

# Before the check ends, the dict will be printed to handle the data
print(dict_string)

# Once we have the dict with the data we can handle our dirty dates, then check them again until it's all cleaned.
# Then we can check our data with spreadsheet or with SQL, for SQL we can work with pandas library, but by now this is enough
# to understand some basics of data scraping and data cleaning.