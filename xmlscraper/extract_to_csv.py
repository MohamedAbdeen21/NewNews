import psycopg2 as pg
import csv
import xmlscraper.properties as properties

def run():
    con = pg.connect("host=localhost dbname=newsscraper port=5432 user=spiders password=12345678")
    cur = con.cursor()
    cur.execute("""SELECT * FROM articles WHERE date = %s""",(properties.today_string,))

    with open(f'/home/mohamed/Semester6/PBL/newsscraper/xmlscraper/csvfiles/{properties.today_string}.csv', 'w', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['id','url','title','text','count','date','tags'])
        writer.writerows(cur.fetchall())
