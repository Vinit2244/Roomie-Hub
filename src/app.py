from flask import Flask, request, render_template
import sqlite3

# Setup for flask app and database
app = Flask(__name__)
SQLITE_DB = "database.db"

# This function takes argument as a string form of query to be executed > executes the query and returns the result obtained
# example:
# query_db("""CREATE TABLE IF NOT EXISTS songs (id, name, img, artist, album, duration, UNIQUE(id));""")
def query_db(*args, **kw_args):
    con = sqlite3.connect(SQLITE_DB)
    cur = con.cursor()
    result = cur.execute(*args, **kw_args).fetchall()
    con.commit()
    cur.close()
    con.close()
    return result


@app.route('/')
def load_website():
    return render_template('Main-Pages/index.html')


if __name__ == '__main__':
    app.run(debug=True)