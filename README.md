# mcdonalds_products_parser

> This python script can help to mine data from McDonalds and migrate collected data to MS SQL Server.
> This project is developed only with learning pourposes.

#### items_parser.py
Parses all html files from `files` directory and produce `temp_dataframe.csv` dataset, that contains a product `id`, `title`, `link` to a page with more details, `picture` url and a list of `categories`.

#### load_details_selenium.py
Loops through the products (temp_dataframe.csv) and load more details, such as `description`, `nutritions` and `ingredients`, which is then is exported to `mac_dataframe.csv` dataset. 

#### fin_data_getter.py
By using of `mac_dataframe.csv` dataset generates a new txt file with 'sql inserts', that than can be migrated to a RDBMS.

#### Prerequisites
```
pip install selenium
pip install pandas
pip install beautifulsoup4
```
