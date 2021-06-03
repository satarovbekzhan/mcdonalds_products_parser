from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
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
    if (row['id'] == 20005):
        break

    data['id'].append(row['id'])
    data['title'].append(row['title'])
    data['link'].append(row['link'])
    data['picture'].append(row['picture'])
    data['categories'].append(row['categories'])

    print('Collecting data for:', index, row['id'])

    path = 'C:\\Users\\satar\\OneDrive\\Desktop\\macdonalds\\parser\\products'
    name = row['id']
    f = f'%s\%s.html' % (path, name)
    with open(f, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        data['description'].append(soup.find_all('p', class_="product-detail__description")[0].text)

        data['ingredients'].append(soup.find_all('p', class_="statement ng-binding")[0].text)

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



df_final = pd.DataFrame(data, columns=['id', 'title', 'link', 'description', 'picture', 'categories', 'nutritions', 'ingredients'])

df_final.to_csv(r'C:\Users\satar\OneDrive\Desktop\macdonalds\parser\mac_dataframe.csv', index = False, header=True, encoding='utf-8')

print(df_final)
