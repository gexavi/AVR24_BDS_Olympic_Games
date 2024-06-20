from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# lien vers les données WA yes activé
BASE_RESULTS_LINK = "https://worldathletics.org/competition/calendar-results?hideCompetitionsWithNoResults=true&page=1&offset="

# liste pour stocker les liens extraits de toutes les pages
all_result_links = []

# Selenium
driver = webdriver.Chrome() 

# boucle pour chaque page
for offset in range(0, 15400, 100):  # 154 pages à scraper
    
    page_link = BASE_RESULTS_LINK + str(offset)
    
    # Ouvrir la page avec Selenium
    driver.get(page_link)
    
    # timer de pause
    time.sleep(10)
    html_content = driver.page_source
    
    # BeautifulSoup parsing
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extraire les liens <a> de la page avec le href qui est suivi des eventIds et les ajouter à la liste
    result_links = soup.find_all('a', href=lambda href: href and href.startswith("/competition/calendar-results/results/"))
    all_result_links.extend(result_links)
    
# fermer le navigateur à la fin
driver.quit()

# sauvegarder les liens extraits dans un fichier texte
with open('result_links.txt', 'w') as file:
    # écrire chaque lien dans une nouvelle ligne
    for link in all_result_links:
        file.write(link.get('href') + '\n')