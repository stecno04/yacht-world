# due funzioni una di scraping e una di ricerca link nel sito
# la funzione di scraping prende in input un link e restituisce una lista di link
# la funzione di ricerca naviga il sito e copia tutti i link in una lista

from bs4 import BeautifulSoup as bs
import requests
import os
import json
from tenacity import retry, stop_after_attempt, wait_fixed
import sys 



# Creazione file csv se non esiste
if not os.path.isfile('yacht.json'):
    with open('yacht.json', 'w', encoding='utf-8') as f:
        f.write('[]')

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))  # Retry 3 times with a 5-second delay between retries

def salvataggio(caratteristiche):
    # Load existing data
    existing_data = []
    if os.path.isfile('yacht.json'):
        with open('yacht.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

    link = caratteristiche["link"]  # Access the link value using the key "link"
    characteristics_dict = {key: value for key, value in caratteristiche.items() if key != "link"}
    
    # Check if the link is already present
    existing_links = [entry['link'] for entry in existing_data]
    if link not in existing_links:
        characteristics_dict['link'] = link
        existing_data.append(characteristics_dict)

    # Save the updated data
    with open('yacht.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    return 0

def scraping(link):
    try:
        page = requests.get(link)
        soup = bs(page.content, 'html.parser')
        caratteristiche = {}  # Change caratteristiche from a list to a dictionary

        caratteristiche["link"] = link
        type_of_boat_element = soup.find('a', {'title': 'Power'}) or soup.find('a', {'title': 'Sail'})
        type_of_boat = type_of_boat_element.get_text() if type_of_boat_element else None
        caratteristiche["type m/s"] = type_of_boat

        # Check if the element was found before accessing attributes
        titolo_element = soup.find('h1', class_='heading')
        caratteristiche["titolo"] = titolo_element.text if titolo_element else None

        descrizione_element = soup.find('div', class_='description')
        caratteristiche["descrizione"] = descrizione_element.text if descrizione_element else None

        cash_element = soup.find('span', class_='payment-total')
        caratteristiche["cash"] = cash_element.text if cash_element else None

        location_element = soup.find('h2', class_='location')
        caratteristiche["location"] = location_element.text if location_element else None

        details_container = soup.find("div", class_="collapse-content-details open")

        if details_container:
            details_table = details_container.find("table", class_="datatable-section")
            
            if details_table:
                data_points = details_table.find_all("tr", class_="datatable-item")
            
                # Loop through data points and extract key-value pairs
                scraped_data = {}
                for data_point in data_points:
                    title = data_point.find("td", class_="datatable-title").text
                    value = data_point.find("td", class_="datatable-value").text
                    scraped_data[title] = value
                caratteristiche["scraped_data"] = scraped_data
            else:
                print("Details table not found.")
        else:
            print("Details container not found.")

            
        propulsion_container = soup.find("div", class_="detail-data-table propulsion")
        if propulsion_container:
            engine_categories = propulsion_container.find_all("div", class_="datatable-category")

            engine_details = []
            for engine_category in engine_categories:
                engine_data = {}
                engine_name = engine_category.find("h3", class_="sub-title").text.strip()
                engine_data["Engine Name"] = engine_name

                details_table = engine_category.find("table", class_="datatable-section")
                det = details_table.find_all("tr", class_="datatable-item")
                for data_point in det:
                    title = data_point.find("td", class_="datatable-title").text
                    value = data_point.find("td", class_="datatable-value").text
                    engine_data[title] = value

                engine_details.append(engine_data)
            
            caratteristiche["engine_details"] = engine_details
        else:
            print("No engine details found")


        
        specs_container = soup.find("div", class_="detail-data-table measurements")
        if specs_container:
            specs_categories = specs_container.find_all("div", class_="datatable-category")

            specs_details = []
            for specs_category in specs_categories:
                specs_data = {}
                specs_name = specs_category.find("h3", class_="sub-title").text.strip()
                specs_data["specs"] = specs_name

                details_table = specs_category.find("table", class_="datatable-section")
                det = details_table.find_all("tr", class_="datatable-item")

                for data_point in det:
                    title = data_point.find("td", class_="datatable-title").text
                    value = data_point.find("td", class_="datatable-value").text
                    specs_data[title] = value

                specs_details.append(specs_data)
            
            caratteristiche["specs_details"] = specs_details
        else:
            print("No specs details found")
        
        print(caratteristiche)
        salvataggio(caratteristiche)  # Pass the dictionary directly
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        raise e  # Re-raise the exception to trigger the retry mechanism

    
    return 0

def ricerca():
    min = 143000
    max = 144000
    while True:
        jk = 0
        k = 0
        link = f'https://www.yachtworld.com/boats-for-sale/price-{min},{max}/'
        r = requests.get(link)
        soup = bs(r.text, 'html.parser')
        x = soup.find('div', class_='results-count')
        print(x)
        x, _ = x.text.split(' ')
        print(x)
        x = int(x)
        x = (x // 15) + 2
        print(x)
        for x in range(1, x):
            try:
                link = f'https://www.yachtworld.com/boats-for-sale/price-{min},{max}/page-{x}/'
                r = requests.get(link)
                soup = bs(r.text, 'html.parser')

                print(link)
                lista = []
                lista_vecchia = lista
                
                lista = soup.find_all('a', href=True)
                lista = [i for i in lista if i['href'].startswith('/yacht/')]
                if lista == lista_vecchia:
                    break
                if len(lista) == 0:
                    break
                else:
                    len_lista = len(lista) 
                    jk = 0
                    for i in lista:
                        print(i['href'])
                        # check if the link is already present
                        link_art = 'https://www.yachtworld.com' + i['href']
                        with open('yacht.json', 'r', encoding='utf-8') as f:
                            existing_data = json.load(f)
                        existing_links = [entry['link'] for entry in existing_data]
                        if link_art not in existing_links:
                            print(link)
                            scraping(link_art)
                            jk = 0
                            k = 0
                        else:
                            jk += 1
                            if jk == len_lista:
                                k += 15
                                jk = 0
                            print(f'len_lista = {len_lista},                     jk = {jk},                  k = {k}')
                            print(f'')

                            print('link già presenteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                            if k > 500:
                                for _ in range(50):
                                    print('presenteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                                x = 250
                                jk = 0 

            except requests.exceptions.RequestException as e:
                print("Error:", e)
                raise e  # Re-raise the exception to trigger the retry mechanism

            
            
        if max == 1550005000:
            sys.exit()
        min += 1000
        max += 1000

def main():
    ricerca()
    while True:
        k = input("desideri aggiungere un link alla lista preferiti? (y/n) ")
        if k == "y":
            link = input("inserisci il link: ")
            scraping(link)
        else:
            print("ok")
            break

main()