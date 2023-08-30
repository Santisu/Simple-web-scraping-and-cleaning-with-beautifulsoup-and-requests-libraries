
# First import the libraries that we will use, remember to install the requeriments.txt
import csv
import os
import datetime
import requests
from bs4 import BeautifulSoup


# Set a dictionary with the months so it can be converted from string to int once scraped
meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'setiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}
# First we get the directory were is stored the script...
ruta_script = os.path.dirname(os.path.abspath(__file__))
# Then we select the file were our data will be stored
registro_csv = os.path.join(ruta_script, 'one_piece_manga.csv')

# If the CSV file doesn't exists it will be created, opened in write mode and create headers for each column (the first line)
if not os.path.exists(registro_csv):
    with open(registro_csv, 'w') as f:
        f.write("capitulo, volumen, titulo, titulo_romanizado, descripcion_portada, portada_color, fecha\n")

# Set the var for the url
numero_url = 1

# Set the count of null values
total_null_values = 0
# Get the hour were the scraping starts
hora_inicio = datetime.datetime.now().time()

# Through a while loop our script will iterate on every chapter's page and get the data that we want

# The loop will end to the last register known to the current date
while numero_url < 1090:
    # Using 'requests' we will get the page of the chapter, it will go to the next one on every iteration
    r = requests.get(f'https://onepiece.fandom.com/es/wiki/Cap%C3%ADtulo_{numero_url}')
    # Using BeautifulSoup the first argument (r.text) gets the text from the html,
    # the second argument (lxml) specifies the parser that we will use to interpret the text
    soup = BeautifulSoup(r.text, 'lxml')

    # Each specific data will be stored on a list that we will use to write on the csv file
    registro = []


    """
    Exctructure for each scrap:
        - We will use a "try-except" sentence to get our data. A successfull scrap will be excecuted in the try sentence,
        if there is any problem, like the tag doesnt exist or the data wasn't added in the font web, the exception will be 
        catched in the except sentence, and the data will be stored as 'null'.
        - Once the specific data is setted, whatever if its a real value or null, it will be added to the list, for the cases
        that we want a string, we are going to add cuotation marks ("") to secure that the commas from a text wont corrupt our CSV.

    Beautiful Soup Methods:
        .find(): Finds and returns an element that matches the provided argument, which can be any HTML attribute. 
        .get_text(): Retrieves the plain text content from a selected tag, excluding any nested inner tags. 

    Beautiful Soup Attribute:
        .parent: An attribute that lets you access the parent tag of the current tag in the parsed HTML. 
    """

    # Capítulo

    try:
        # First get the data through a specific class and get the text
        capitulo_bruto = soup.find(class_='page-header__title').get_text()
        # The structure of the title is "Capitulo X", we want the X value so we split the text...
        capitulo_list = capitulo_bruto.split(' ')
        # ...and take only the last element which contains the number
        capitulo = capitulo_list[1]
    except:
        capitulo = 'null'
    # Finally we append the value in our list
    registro.append(capitulo)

    # Volumen
    try:
        # For this case we will user the 'data-source' attribute so we declare the value of the attribute...
        volumen_data_source = 'vol'
        # ...then find the element with the same name and then extract their values, before this we make sure that the value is in a unique tag.
        volumen_bruto = soup.find(attrs={'data-source': volumen_data_source})
        # Finally we seek for the tag with the class that is inside the 'volumen_bruto' var, and get the text
        volumen = volumen_bruto.find(class_='pi-data-value').get_text()
        # If the value isnt a number it will be set as null
        if not volumen.isdigit():
            volumen = 'null'
    except:
        volumen = 'null'

    registro.append(volumen)

    # Título
    try:
        # Easy peasy
        titulo = soup.find(class_='pi-title').get_text()
    except:
        titulo = 'null'

    registro.append('"'+ titulo + '"')

    # Título romanizado
    try:
        # Same as with 'volumen'
        titulo_ro_data_source = 'nombrero'
        titulo_romaji_bruto = soup.find(attrs={'data-source': titulo_ro_data_source})
        titulo_romaji = titulo_romaji_bruto.find(class_='pi-data-value').get_text()
    except:
        titulo_romaji = 'null'

    registro.append('"'+ titulo_romaji + '"')

    # Descripción portada
    try:
        # For this case, 'descripción portada' doesn't have a specific class, id or tag, it's just a <p> tag, so we search for a reference.
        descripcion_referencia = soup.find(id='Portada')
        # Once we find our consistent reference, we navigate to the data that we want,
        # in this case our reference is a child of a same-level tag next to our desired data
        padre = descripcion_referencia.parent
        # Using find find_next method we finally are in the tag that contains our data
        descripcion_portada = padre.find_next('p')
        # Now we almost have our data, but... In some pages it isn't the unique information, so we gotta prepare some cases
        primer_get = descripcion_portada.get_text().lower()
        # In some cases there is a previous tag with irrelevant info as the number of pages and the volumen, all wrapped in a <p> tag.
        # For those cases we will seek for the next <p> tag and rewrite 'descripcion_portada' to store the next tag 
        if 'pg' in primer_get or 'pág' in primer_get:
            descripcion_portada = descripcion_portada.find_next('p')
        # There are some cases where the cover is a color one, in those cases the description includes 'portada a color', thats irrelevant
        # info, and can be stored as a specific value, so we split the text and drop that info off, but we keep it apart and save.
        # With the method .replace() we make sure that there will not be a linebreak on the string, so it can be more easy to read and analyse
        if 'portada a color' in descripcion_portada.get_text().lower() or 'portadas a color' in descripcion_portada.get_text().lower():
            cortada = descripcion_portada.get_text().split(' ')
            descripcion_portada = ' '.join(cortada[3:]).replace('\n', ' ')
            portada_color = 1
        else:
            descripcion_portada = descripcion_portada.get_text().replace('\n', ' ')
            portada_color = 0
    except:
        descripcion_portada = 'null'
        portado_color = 'null'

    registro.append('"'+ descripcion_portada + '"')
    registro.append(portada_color)


    # Fecha de lanzamiento
    try:
        # First we get the data through its specific attribute
        fecha_data_source = 'fecha'
        fecha_bruto = soup.find(attrs={'data-source': fecha_data_source}).div.string
        # The split it for year. We know that first is day and last is year
        fecha_cortada = fecha_bruto.split(' ')
        print(fecha_cortada)
        anno = fecha_cortada[-1].strip(',').strip(' ')
        mes = (fecha_cortada[2]).lower().strip(',').strip(' ')
        dia = fecha_cortada[0].strip(',').strip(' ')
        # Now we convert the month string to int, and if there is some typo and it doesn match we will set a name to handle it later
        check = True
        for m, numero in meses.items():
            if m == mes:
                mes = str(numero)
                check = False
                break
        if check:
            mes = 'month_error'
        # We also could use regular expressions the check that it has the correct format, by now this is enough
        print(mes)
        # Store the date on a desired format...      
        fecha_list = [anno, mes, dia]
        # And join it separated with '-'
        fecha = '-'.join(fecha_list)
    except:
        fecha = 'null'

    registro.append(fecha)


    # Finally we open our csv and create a new row with our data
    with open(registro_csv, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(registro)

    # Set an individual print for each scrap, in case of some null it will print which chapter has nulls
    nulo = ''
    for reg in registro:
        if reg == 'null':
            nulo = 'with null'
            total_null_values += 1
            break
    print(f'Capítulo {capitulo} agregado {nulo}')

    # And increase the number to scrap the next chapter page
    numero_url += 1


# Once the while loop ends we get time where it stops and print both start and finish

hora_termino = datetime.datetime.now().time()
print(f"El total de valores nulos fue de: {total_null_values}")
print("Hora inicio: ", hora_inicio.strftime("%H:%M:%S"))
print("Hora termino: ", hora_termino.strftime("%H:%M:%S"))


# El total de valores nulos fue de: 57 - Having some clarity about how much null values are can help us to know if we have to review our script or our fonts
# Hora inicio:  19:19:40
# Hora termino:  19:25:02

# Now that we have our data stored, for this example we are going to check
# that the dates are in correct format using the date_verifier script