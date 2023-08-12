# due funzioni una di scraping e una di ricerca link nel sito
# la funzione di scraping prende in input un link e restituisce una lista di link
# la funzione di ricerca naviga il sito e copia tutti i link in una lista

from bs4 import BeautifulSoup as bs
import requests
import re
import os


def salvataggio(caratteristiche):
    return 0

def scraping(link):
    
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