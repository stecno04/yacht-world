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

def ricerca(min, max):
    diff = max - min
    diff = diff / 1000
    jj = 0
    max = min + 1000
    while jj <= diff:
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
                # find all <a class="inner" data-reporting-click-product-id="9007541" data-reporting-click-listing-type="standard listing" data-reporting-rank="1" data-reporting-page="1" href="/yacht/2020-sacs-sacs-strider-10-9007541/"><div class="image-container"><div class="dummy"></div><div class="image"><div class="banner-attribute NEW_ARRIVAL">Nuovo arrivo</div><div class="icons"></div><img alt="SACS Sacs STRIDER 10" class="image-results" height="222" loading="eager" fetchpriority="high" src="https://images.boatsgroup.com/resize/1/75/41/9007541_20230821040450392_1_XLARGE.jpg?w=300&amp;h=222&amp;t=1692615891000&amp;exact" width="300"></div></div><div class="description"><div class="top"><div class="name"><h2 class="">2020 SACS Sacs STRIDER 10</h2></div><div class="price">165.000 €*</div><div class="location">Dubrovnik, Croazia<div>990m<!-- --> - <!-- -->2020</div></div></div><div class="bottom"><div class="offered-by">Euromarine d.o.o.</div></div></div></a>
                # where href starts with /yacht/
                lista = soup.find_all('a', href=True)
                lista = [i for i in lista if i['href'].startswith('/yacht/')]
                print(lista)
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
                    else:
                        print(f'')
                        print('link già presenteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

            except requests.exceptions.RequestException as e:
                print("Error:", e)
                raise e  # Re-raise the exception to trigger the retry mechanism

            
            
        if max == 1550005000:
            sys.exit()
        min += 1000
        max += 1000
        jj = jj + 1

def main():
    while True:
        k = input("Would you like to update the dataset or add manually a single link? 1: update, 2: add single, 3: add multiples links, 0: exit ")
        if k == "2":
            link = input("inserisci il link: ")
            scraping(link)
        elif k =="1":
            min = int(input("inserisci prezzo minimo di ricerca "))
            max = int(input("inserisci massimo prezzo di ricerca "))
            ricerca(min, max)
        elif k == "3":
            link = input("inserisci link, 0 for exiting ")
            while len(link) > 1:
                scraping(link)
                link = input("inserisci link, 0 for exiting ")
        elif k == "0":
            break
        else:
            print("wrong input, retry")
                


main()