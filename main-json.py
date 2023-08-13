# due funzioni una di scraping e una di ricerca link nel sito
# la funzione di scraping prende in input un link e restituisce una lista di link
# la funzione di ricerca naviga il sito e copia tutti i link in una lista

from bs4 import BeautifulSoup as bs
import requests
import os
import json


# Creazione file csv se non esiste
if not os.path.isfile('yacht.json'):
    with open('yacht.json', 'w', encoding='utf-8') as f:
        f.write('[]')

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

    page = requests.get(link)
    soup = bs(page.content, 'html.parser')
    caratteristiche = {}  # Change caratteristiche from a list to a dictionary
    
    caratteristiche["link"] = link
    type_of_boat_element = soup.find('a', {'title': 'Power'}) or soup.find('a', {'title': 'Sail'})
    type_of_boat = type_of_boat_element.get_text() if type_of_boat_element else None
    caratteristiche["type m/s"] = type_of_boat
    caratteristiche["titolo"] = soup.find('h1', class_='heading').text
    caratteristiche["descrizione"] = soup.find('div', class_='description').text
    caratteristiche["cash"] = soup.find('span', class_='payment-total').text
    caratteristiche["location"] = soup.find('h2', class_='location').text
    
    details_container = soup.find("div", class_="collapse-content-details open")

    # Find the details table within the container
    details_table = details_container.find("table", class_="datatable-section")

    # Extract individual data points
    data_points = details_table.find_all("tr", class_="datatable-item")

    # Loop through data points and extract key-value pairs
    scraped_data = {}
    for data_point in data_points:
        title = data_point.find("td", class_="datatable-title").text
        value = data_point.find("td", class_="datatable-value").text
        scraped_data[title] = value
    caratteristiche["scraped_data"] = scraped_data
    
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
    return 0

def ricerca():
    x = 1
    while True:
        link = f'https://www.yachtworld.com/boats-for-sale/page-{x}/'
        print(link)
        r = requests.get(link)
        soup = bs(r.text, 'html.parser')
        lista = soup.find_all('a', href=True)
        if len(lista) == 0:
            break
        else:
            for i in lista:
                if i['href'].startswith('/yacht/'):
                    print(i['href'])
                    # check if the link is already present
                    link = 'https://www.yachtworld.com' + i['href']
                    with open('yacht.json', 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                    existing_links = [entry['link'] for entry in existing_data]
                    if link not in existing_links:
                        scraping(link)
                    else:
                        print('link già presenteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

        x += 1
    return 0

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