from flask import Flask, request, render_template, url_for
from forms import SignUpForm, SignInFormEmail, SignInFormUsername
import sqlite3

# Setup for flask app and database
app = Flask(__name__)

app.config['SECRET_KEY'] = '1974bf4e181357512bf418984285ad45'

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


@app.route('/signUp')
def signUp():
    form = SignUpForm()
    return render_template('Forms/signUp.html', form=form)

@app.route('/signInEmail')
def signInEmail():
    form = SignInFormEmail()
    return render_template('Forms/signInEmail.html', form=form)

@app.route('/signInUsername')
def signInUsername():
    form = SignInFormUsername()
    return render_template('Forms/signInUsername.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)