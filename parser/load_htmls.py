from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
df = pd.read_csv('temp_dataframe.csv')

for index, row in df.iterrows():
    print('Fetching html of:', index, row['link'])
    time.sleep(2)
    r = requests.get(row['link'], timeout=15, headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    path = 'C:\\Users\\satar\\OneDrive\\Desktop\\macdonalds\\parser\\products'
    name = row['id']
    f = f'%s\%s.html' % (path, name)
    with open(f, 'w', encoding='utf-8') as file:
        file.write(r.text)
