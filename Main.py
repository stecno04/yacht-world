# due funzioni una di scraping e una di ricerca link nel sito
# la funzione di scraping prende in input un link e restituisce una lista di link
# la funzione di ricerca naviga il sito e copia tutti i link in una lista

from bs4 import BeautifulSoup as bs
import requests
import re
import os


def salvataggio(caratteristiche):
    # salvataggio caratteristiche in un file csv
    # creazione file csv se non esiste
    if not os.path.isfile('yacht.csv'):
        with open('yacht.csv', 'w') as f:
            f.write('link, titolo, descrizione, prezzo, paese, anno, lunghezza, fuel type, hull material, model\n')
    # salvataggio caratteristiche nel file csv
    with open('yacht.csv', 'a') as f:
        # salva le caratteristiche sono se non sono già presenti nel file quelle con lo stesso link
        if not caratteristiche[0] in f.read(): 
            f.write(caratteristiche[0] + ',' + caratteristiche[1] + ',' + caratteristiche[2] + ',' + caratteristiche[3] + ',' + caratteristiche[4] + ',' + caratteristiche[5] + ',' + caratteristiche[6] + ',' + caratteristiche[7] + ',' + caratteristiche[8] + ',' + caratteristiche[9] + '\n')
    
    return 0

def scraping(link):
    # creazione lista caratteristiche [link, titolo, descrizione, prezzo, paese, anno, lunghezza, fuel type, hull material, model]
    # esempio link: https://www.yachtworld.com/yacht/2023-azimut-50-fly-8990909/
    page = requests.get(link)
    soup = bs(page.content, 'html.parser')
    caratteristiche = []
    caratteristiche.append(link)
    caratteristiche.append(soup.find('h1', class_='heading').text)
    caratteristiche.append(soup.find('div', class_='description').text)
    caratteristiche.append(soup.find('span', class_='payment-total').text)
    
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
        caratteristiche.append(value)
    print(caratteristiche)
    salvataggio(caratteristiche)
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