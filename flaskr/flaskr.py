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
current_user = None

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'User({self.name}, {self.email})'

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


def query_db(query, args=(), one=False):
    print("HEY")
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    return rv if rv else None


@app.route('/')
def show_entries():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    mood = query_db('select date, happiness from Mood where email = (?) order by date desc', [current_user.email])
    return render_template('show_entries.html', mood=mood, user=current_user)


@app.route('/add', methods=['POST'])
def add_entry():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    query_db('insert into Mood (email, date, happiness) values (?, ?, ?)',
             [current_user.email, request.form['date'], request.form['happiness']])
    print([x['date'] for x in query_db('select date, happiness from Mood where email = (?) order by date desc', [current_user.email])])
    flash('New mood was successfully posted.')
    return redirect(url_for('show_entries'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global current_user
    if session.get('logged_in') and current_user:
        return redirect(url_for('show_entries'))
    error = None
    if request.method == 'POST':
        if request.form['email'] not in query_db('select email from RegisteredUser'):
            query_db('insert into RegisteredUser (name, email) values(?,?)', 
                     [request.form['name'], request.form['email']])
            flash('You have successfully signed up.')
            return redirect(url_for('login'))
        else:
            error = 'You have already signed up'
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    error = None
    if request.method == 'POST':
        q = [x['email'] for x in query_db('select email from RegisteredUser')]
        p = [x['password'] for x in query_db('select password from RegisteredUser where email = ?', [request.form['email']])]
        if request.form['email'] not in q:
            error = 'Invalid email. If you do not have an account, please sign up.'
        elif request.form['password'] not in p:
            error = 'Invalid password for this email.'
        else:
            user = query_db('select * from RegisteredUser where email = ?', [request.form['email']])
            name, email = user[0]['name'], user[0]['email']
            current_user = User(name, email)
            print(current_user)

            session['logged_in'] = True
            flash(f'Welcome Back, {name}!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    global current_user
    if not session['logged_in']:
        return redirect(url_for('login'))
    current_user = None
    session['logged_in'] = False
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
