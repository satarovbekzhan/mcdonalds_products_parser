from bs4 import BeautifulSoup

def get_parsed_item_from_li(li):
    title = li.find_all('span', class_="categories-item-name")[0].text
    link = li.find_all('a', class_="categories-item-link")[0]['href']
    picture = 'https://www.mcdonalds.com' + li.find_all('source')[1]['srcset']
    return [title, link, picture, [], '']


def get_items_from_html(html):
    items = []
    soup = BeautifulSoup(html, 'lxml')
    category = soup.find_all('h1', class_="mcd-category-page__main-content__title")[0].text
    for li in soup.find_all('li', class_="categories-list-item"):
        item = get_parsed_item_from_li(li)
        item[3].append(category)
        items.append(item)
    return items

path = 'C:\\Users\\satar\\OneDrive\\Desktop\\macdonalds\\files'
sources = [
    'Actionsproducte.html',
    'Beilagen.html',
    'Burger & McNuggets.html',
    'Desserts.html',
    'Frucht-Kick.html',
    'Frühstück.html',
    'Getränke.html',
    'Iced Drinks.html',
    'McCafé Drinks.html',
    'McCafé Food.html',
    'McFlurry.html',
    'McMilchshake.html',
    'McWraps.html',
    'Salate.html',
    'Saucen & Dressings.html',
    'Signature Collection.html'
]

products = []

def collect(item):
    added = False
    for i, p in enumerate(products):
        if (p[0] == item[0]):
            added = True
            products[i][3].append(item[3][0])
            break
    if (not added):
        products.append(item)

for source in sources:
    file_path = '{0}\{1}'.format(path, source)
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        items_list = get_items_from_html(html)
        for item in items_list:
            collect(item)
            
id = 19900
for i, p in enumerate(products):
    p[4] = id
    id = id + i + 1

import pandas as pd

data = {
    'id': [],
    'title': [],
    'link': [],
    'picture': [],
    'categories': [] 
}

for p in products:
    data['id'].append(p[4])
    data['title'].append(p[0])
    data['link'].append(p[1])
    data['picture'].append(p[2])
    data['categories'].append(p[3])
    # print(p[4])

df = pd.DataFrame(data, columns=['id', 'title', 'link', 'picture', 'categories'])

df.to_csv(r'C:\Users\satar\OneDrive\Desktop\macdonalds\parser\temp_dataframe.csv', index = False, header=True, encoding='utf-8')

print(df.to_string())
