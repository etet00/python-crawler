import requests
import mysql.connector
from mysql.connector import errorcode


# 測試與 MySQL server 的連線是否正常
try:
    cnx = mysql.connector.connect(user="xxxx", password="xxxxx", host='127.0.0.1')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Successfully connect to MySQL server")

cursor = cnx.cursor()


# 建立 MySQL DATABASE
DB_NAME = "pchome"


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


# 建立 tables

TABLES = {}
TABLES['pchome_products'] = (
    "CREATE TABLE `pchome_products` ("
    "  name varchar(60) NOT NULL,"
    "  price varchar(7) NOT NULL,"
    "  PRIMARY KEY (name)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# 從 pchome 上面抓取商品資料，並將資料輸入到 table 中
add_product = ("INSERT IGNORE　INTO pchome_products"
               "(name, price) "
               "VALUES (%s, %s)")
url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=ps4&page=1&sort=sale/dc"
re = requests.get(url)
if re.status_code == requests.codes.ok:
    data = re.json()
    prods = data["prods"]
    for prod in prods:
        name = prod["name"]
        price = prod["price"]
        if len(name) > 60:
            name = name[:60]
        print(name, price)
        data_product = (name, price)
        cursor.execute(add_product, data_product)


# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
