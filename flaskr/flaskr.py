import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)  # create the application instance
app.config.from_object(__name__)  # load config from this file, flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'create.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

idCount = 0


class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def load_db():
    db = get_db()
    with app.open_resource('load.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.cli.command('test_queries')
def test():
    db = get_db()
    t = None
    with app.open_resource('test-sample.sql', mode='r') as f:
        r = db.cursor().executescript(f.read())
        t = r.fetchall()
    print(t)
    db.close()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    load_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select user_id, date, happiness from Mood order by user_id desc')
    mood = cur.fetchall()
    db.close()
    return render_template('show_entries.html', mood=mood)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into Mood (user_id, date, happiness) values (?, ?, ?)',
               [request.form['user_id'], request.form['date'], request.form['happiness']])
    db.commit()
    flash('New mood was successfully posted.')
    return redirect(url_for('show_entries'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if session.get('logged_in'):
    #     abort(401)
    error = None
    db = get_db()
    if request.method == 'Post':
        if request.form['id'] not in query_db('select id from RegisteredUser'):
            # may want to use auto increment
            db.execute('insert into RegisteredUser (id, name, email) values(?,?,?)',
                       [request.form['id'], request.form['name'], request.form['email']])

            # would add this to database
            db.commit()
            flash('You have successfully signed up.')
            return redirect(url_for('login'))
        else:
            error = 'User ID is taken'
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in query_db('select id from RegisteredUser'):
            error = 'Invalid username'
        elif request.form['password'] not in query_db('select password from RegisteredUser where id = ()'):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
