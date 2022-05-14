from flask import Flask, render_template, request, make_response, redirect
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from xmlscraper.properties import today_string

app = Flask(__name__)

def get_connection():
        con = pg.connect("""host=localhost
                          dbname=newsscraper
                          port=5432
                          user=spiders
                          password=12345678""")
        return con

def execute_select(for_user=False, user=1):
    con = get_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)
    if for_user:
        cur.execute(f"""SELECT title, url , tags
                        FROM articles 
                        WHERE date = '{today_string}' and tags != 'NULL'
                        OFFSET {5 * int(user) - 1}
                        LIMIT 5""")
    else:
        cur.execute(f"""SELECT title, url, tags
                        FROM articles 
                        WHERE date = '{today_string}' and tags != 'NULL'
                        LIMIT 50""")
    return cur.fetchall()

def execute_visit(userId = None, url = None):
    if userId == None or url == None:
        raise ValueError
    else:
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("""INSERT INTO users_articles(user_id,article_id) 
                            SELECT %s, sk FROM articles WHERE url = %s
                            ON CONFLICT DO NOTHING""",(userId,url))
            con.commit()
        except pg.IntegrityError as exception:
            print(repr(exception))
            cur.execute("ROLLBACK")
            cur.execute("""INSERT INTO users(id,some_feature) VALUES(%s,'x')""",(userId,))
            cur.execute("""INSERT INTO users_articles(user_id,article_id) 
                            SELECT %s, sk FROM articles WHERE url = %s
                            ON CONFLICT DO NOTHING""",(userId,url))
            print('added')
            con.commit()

@app.route('/', methods = ['POST','GET'])
def index():
    userId = request.cookies.get('userID')
    if not userId:
        userId = 1
    personalized = execute_select(for_user=True,user=userId)
    daily_data = execute_select(for_user=False)
    resp = make_response(render_template('index.html',daily_rows = daily_data, recommendation = personalized, user = userId))
    if request.method == 'POST':
        userId = request.form['name']
        personalized = execute_select(for_user=True,user=userId)
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', userId)
    return resp

@app.route('/redirect/<path:pars>')
def open_url(pars):
    userId = request.cookies.get('userID')
    if not userId:
        userId = 1
    execute_visit(userId, pars)
    return redirect(pars)

if __name__ == '__main__':
    app.run(debug=True)