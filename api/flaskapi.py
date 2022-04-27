from flask import Flask, render_template, request, make_response
import psycopg2 as pg
from xmlscraper.properties import today_string

app = Flask(__name__)
def get_connection():
        con = pg.connect("""host=localhost
                          dbname=newsscraper
                          port=5432
                          user=spiders
                          password=12345678""")
        return con

@app.route('/', methods = ['POST','GET'])
def index():
    con = get_connection()
    cur = con.cursor()
    if request.method == 'POST':
        user = request.form['name']
        cur.execute(f"""SELECT title, url 
                        FROM articles 
                        WHERE date = '{today_string}'
                        OFFSET {5 * int(user) - 1}
                        LIMIT 5""")
        data = cur.fetchall()
        resp = make_response(render_template('personal.html',rows = data, user = user))
        resp.set_cookie('userID', user)
        return resp
    else:
        USER_ID = request.cookies.get('userID')
        cur.execute(f"""SELECT title, url 
                        FROM articles 
                        WHERE date = '{today_string}'
                        LIMIT 50""")
        data = cur.fetchall()
        return render_template('index.html',rows = data, user = USER_ID)

if __name__ == '__main__':
    app.run(debug=True)