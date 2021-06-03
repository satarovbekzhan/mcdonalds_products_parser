import pandas as pd


df = pd.read_csv('mac_dataframe.csv')

# load all gategories ##########################################
categories = []
c_id = 10

def add_category(name):
    global c_id
    added = False
    for c in categories:
        if c['name'] == name:
            added = True
    if not added:
        c_id = c_id + 1
        categories.append({
            'id': c_id,
            'name': name
        })


for index, row in df.iterrows():
    names = row['categories'][1:-1].split(", ")
    for name in names:
        add_category(name[1:-1])

# ##################################################################


# load all nitrients and units #####################################
nutrients = []
units = []

n_id = 10
def add_n(name):
    global n_id
    added = False
    for n in nutrients:
        if n['name'] == name:
            added = True
    if not added:
        n_id = n_id + 1
        nutrients.append({
            'id': n_id,
            'name': name
        })

u_id = 10
def add_u(name):
    global u_id
    added = False
    for c in units:
        if c['name'] == name:
            added = True
    if not added:
        u_id = u_id + 1
        units.append({
            'id': u_id,
            'name': name
        })


for index, row in df.iterrows():
    nutr_rows = row['nutritions'][2:-2].split("], [")
    for nutr_row in nutr_rows:
        nutrs = nutr_row.split(", ")
        n = nutrs[0][1:-1]
        u = nutrs[1][1:-1]
        # g = nutrs[2][1:-1]
        # p = nutrs[3][1:-1]
        add_n(n)
        add_u(u)

# ##################################################################

# final model ########################################

products = []
p_category = []
composition = []
com_id = 10000

def mod_str_val(text):
    d_text = text.replace("'", "''")
    e_text = d_text.replace("\n", " ")
    return e_text
    # mod_str = ''
    # for character in text:
    #     if character  == "'":
    #         mod_str += "''"
    #     else:
    #         mod_str += character
    # res_text = mod_str.replace("\n", " ")
    # return res_text

for index, row in df.iterrows():
    try:
        m_title = mod_str_val(row['title'])
    except:
        m_title = ''

    try:
        m_description = mod_str_val(row['description'])
    except:
        m_description = ''

    try:
        m_ingredients = mod_str_val(row['ingredients'])
    except:
        m_ingredients = ''

    products.append({
        'id': row['id'],
        'title': m_title.rstrip(),
        'description': m_description.rstrip(),
        'picture': row['picture'],
        'ingredients': m_ingredients.rstrip()
    })
    
    for c in categories:
        if c['name'] in row['categories']:
            p_category.append({
                'product': row['id'],
                'category': c['id']
            })
    
    for nutr_row in row['nutritions'][2:-2].split("], ["):
        nutrs = nutr_row.split(", ")
        if (nutrs[2][1:-1] == ''):
            g = '0'
        else:
            g = nutrs[2][1:-1]
        
        if (nutrs[3][1:-1] == ''):
            p = '0'
        else:
            p = nutrs[3][1:-1]
        for n in nutrients:
            for u in units:
                if (n['name'] in nutr_row) and (u['name'] in nutr_row):
                    com_id = com_id + 4
                    composition.append({
                        'id': com_id,
                        'product': row['id'],
                        'nutrient': n['id'],
                        'unit': u['id'],
                        'pro_100': g,
                        'pro_por': p
                    })

# data = {
#     'id': [],
#     'title': [],
#     'link': [],
#     'picture': [],
#     'categories': [],
#     'description': [],
#     'ingredients': [],
#     'nutritions': []
# }

# for l in p_category:
#     print(l)
# 
# print('-----------------------')
# 
# for c in composition:
#     print(c)

with open('insert_data.txt', 'a', encoding='utf-8') as f:
    for c in categories:
        code = f'INSERT INTO category (id, name) VALUES (%s, \'%s\');\n' % (c['id'], c['name'])
        f.write(code)


    for p in products:
        code = f'INSERT INTO product (id, title, description, picture, ingredients) VALUES (%s, \'%s\', \'%s\', \'%s\', \'%s\');\n' % (p['id'], p['title'], p['description'], p['picture'], p['ingredients'])
        f.write(code)


    for n in nutrients:
        code = f'INSERT INTO nutrient (id, name) VALUES (%s, \'%s\');\n' % (n['id'], n['name'])
        f.write(code)


    for u in units:
        code = f'INSERT INTO unit (id, name) VALUES (%s, \'%s\');\n' % (u['id'], u['name'])
        f.write(code)


    for l in p_category:
        code = f'INSERT INTO ref_product_category (product, category) VALUES (%s, %s);\n' % (l['product'], l['category'])
        f.write(code)


    for c in composition:
        code = f'INSERT INTO composition (id, product, nutrient, unit, pro_100, pro_por) VALUES (%s, %s, %s, %s, %s, %s);\n' % (c['id'], c['product'], c['nutrient'], c['unit'], c['pro_100'], c['pro_por'])
        f.write(code)



# ##################################################################

# for c in categories:
#     print(c['id'], c['name'])

# for i in nutrients:
#     print(i['id'], i['name'])

# for i in units:
#     print(i['id'], i['name'])