import psycopg2 as pg
from datetime import datetime, timedelta
import csv

today = datetime.today() - timedelta(days=1)
today_string = datetime.strftime(today, '%Y-%m-%d')
con = pg.connect("host=localhost dbname=newsscraper port=5432 user=spiders password=12345678")
cur = con.cursor()
cur.execute("""SELECT * FROM articles WHERE date = %s""",(today_string,))

with open(f'/home/mohamed/Semester6/PBL/newsscraper/xmlscraper/{today_string}.csv', 'w', encoding='utf8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['id','url','title','text','count','date'])
    writer.writerows(cur.fetchall())