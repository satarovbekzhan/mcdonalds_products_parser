from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import pandas as pd
import time


browser = webdriver.Chrome('./chromedriver')

df = pd.read_csv('temp_dataframe.csv')

data = {
    'id': [],
    'title': [],
    'link': [],
    'picture': [],
    'categories': [],
    'description': [],
    'ingredients': [],
    'nutritions': []
}

for index, row in df.iterrows():
    data['id'].append(row['id'])
    data['title'].append(row['title'])
    data['link'].append(row['link'])
    data['picture'].append(row['picture'])
    data['categories'].append(row['categories'])

    print('Collecting data for:', index, row['id'], row['link'])
    browser.get(row['link'])
    time.sleep(3)

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    try:
        data['description'].append(soup.find_all('p', class_="product-detail__description")[0].text)
    except:
        data['description'].append('no description')
        print("no description")
    
    try:
        data['ingredients'].append(soup.find_all('p', class_="statement ng-binding")[0].text)
    except:
        data['ingredients'].append('no ingredients given')
        print("no ingredients given")
    
    try:
        table = soup.find_all('table', class_="column-wrapper width-manager")[0]
        rows = table.find_all('tr')
        nutritions = []
        for tr in rows[1:]:
            n = tr.find_all('th')[0].find_all('span', class_="marketing-name")[0].text.strip()
            u = tr.find_all('th')[0].find_all('span', class_="marketing-name ng-binding")[0].text.strip()
            v_100 = tr.find_all('td')[0].find_all('span')[0].text.strip()
            v_por = tr.find_all('td')[1].find_all('span')[0].text.strip()
            nutritions.append([n, u, v_100, v_por])
        data['nutritions'].append(nutritions)
    except:
        data['nutritions'].append([])
        print("no nutritions []")

try:
    browser.close()
except:
    print("browser not closed")

df_final = pd.DataFrame(data, columns=['id', 'title', 'link', 'description', 'picture', 'categories', 'nutritions', 'ingredients'])

df_final.to_csv(r'C:\Users\satar\OneDrive\Desktop\macdonalds\parser\mac_dataframe.csv', index = False, header=True, encoding='utf-8')

print(df_final)
