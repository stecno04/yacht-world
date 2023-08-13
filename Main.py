# due funzioni una di scraping e una di ricerca link nel sito
# la funzione di scraping prende in input un link e restituisce una lista di link
# la funzione di ricerca naviga il sito e copia tutti i link in una lista

from bs4 import BeautifulSoup as bs
import requests
import re
import os


# Creazione file csv se non esiste
if not os.path.isfile('yacht.csv'):
    with open('yacht.csv', 'w', encoding='utf-8') as f:
        f.write('link, titolo, descrizione, prezzo, anno, fatta da chi, modello, classe, lunghezza, fuel type, hull material, hull shape, hull warrenty, paese\n')

def remove_non_breaking_spaces(text):
    text.replace('\u00A0', ' ')
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()


def salvataggio(caratteristiche):
    # Salvataggio caratteristiche in un file csv
    
    # Check if the characteristics are already present in the file
    characteristics_line = ' ,/[..]/, '.join(caratteristiche)
    characteristics_line += '\n'
    
    already_present = False
    with open('yacht.csv', 'r', encoding='utf-8') as f:
        for line in f:
            if line == characteristics_line:
                already_present = True
                print('already present 222222222222222222222222222222222222222222222')
                break
    
    # Append the characteristics to the file if not already present
    if not already_present:
        with open('yacht.csv', 'a', encoding='utf-8') as f:
            f.write(characteristics_line)
    
    return 0

def scraping(link):
    # creazione lista caratteristiche [link, titolo, descrizione, prezzo, paese, anno, lunghezza, fuel type, hull material, model]
    link = 'https://www.yachtworld.com' + link

    page = requests.get(link)
    soup = bs(page.content, 'html.parser')
    caratteristiche, lista = [], []
    caratteristiche.append(link)
    caratteristiche.append(f"titolo: {soup.find('h1', class_='heading').text}")
    caratteristiche.append(f"descrizione: {soup.find('div', class_='description').text}")
    caratteristiche.append(f"cash: {soup.find('span', class_='payment-total').text}")
    caratteristiche.append(f"location: {soup.find('span', class_='location').text}")
    
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
    
    for key, value in scraped_data.items():
        cleaned_value = remove_non_breaking_spaces(value)
        caratteristiche.append(f'key:{key}, value: {cleaned_value}'.encode('utf-8').decode('utf-8'))
        
    print(caratteristiche)
    for cara in caratteristiche:
        cara = remove_non_breaking_spaces(cara)
        lista.append(cara.encode('utf-8').decode('utf-8'))  # Convert to utf-8

    salvataggio(lista)
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
                    already_present = False
                    with open('yacht.csv', 'r', encoding='utf-8') as f:  # Change encoding to 'utf-8'
                        for line in f:
                            line = line.split(' ,/[..]/, ')
                            # print(f'lineee : {line[0]}')
                            links = 'https://www.yachtworld.com'+i['href']
                            # print(f'links  : {links}')
                            if line[0] == links:
                                already_present = True
                                print('already present-------------------------------------------------')
                                break
                    
                    if not already_present:
                        scraping(i['href'])

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