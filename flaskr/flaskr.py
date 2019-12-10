import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json

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
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'User({self.name}, {self.email})'

    def _get_activities(self):
        return ["Sleep", "Mood", "Downtime", "Exercise", "Meals", "Work"]


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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def toJson():
    db = get_db()
    db.row_factory = dict_factory
    u = User()
    tables = u._get_activities()
    # for each of the bables , select all the records from the table
    allEntries = []
    for table_name in tables:
        if table_name == "Mood":
            continue
        conn = get_db()
        conn.row_factory = dict_factory
        cur1 = conn.cursor()
        cur1.execute("SELECT * FROM " + table_name)
        results = cur1.fetchall()
        for row in results:
            r = {}
            r['title'] = table_name
            r['start'] = row['start_time']
            r['end'] = row['end_time']
            allEntries.append(r)
            print(results)
        print(allEntries)
    db.close()
    return allEntries


@app.route('/values', methods=['GET'])
def get_all_entries():
    print("here")
    entries = toJson()
    print(entries)
    return json.dumps(entries)


def query_db(query, args=(), one=False):
    # print("HEY")
    db = get_db()
    cursor = db.cursor()
    cur = cursor.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    return rv if rv else None


@app.route('/')
def show_entries():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    mood = query_db('select date, happiness from Mood where email = (?) order by date desc', [current_user.email])
    if mood is None:
        mood = []
    return render_template('show_entries.html', mood=mood, user=current_user)


@app.route('/resize', methods=['POST'])
def entry_resize():
    global current_user
    if not request.form:
        return
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    table_id, e_date, e_start, new_end = request.form['id'], request.form['date'], request.form['start_time'], request.form['end_time']
    print(table_id, e_date, e_start, new_end)
    update = f"update {table_id}"
    query_db(update + ' set end_time = (?) WHERE email = (?) and date = (?) and start_time = (?)', [new_end, current_user.email, e_date, e_start])
    return 'OK'


@app.route('/delete', methods=['POST'])
def delete_entry():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    if not request.form:
        return
    table_id = request.form['id']
    if table_id == "Mood":
        query_db('delete from Mood where email = (?) and date = (?)',
            [current_user.email, request.form['date']])
    elif table_id == "Sleep":
        query_db('delete from Sleep where email = (?) and date = (?) and start_time = (?)',
            [current_user.email, request.form['date'], request.form['start_time']])
    elif table_id == "Exercise":
        query_db('delete from Exercise where email = (?) and date = (?) and start_time = (?)',
            [current_user.email, request.form['date'], request.form['start_time']])
    elif table_id == "Work":
        query_db('delete from Work where email = (?) and date = (?) and start_time = (?)',
                 [current_user.email, request.form['date'], request.form['start_time']])
    elif table_id == "Meals":
        query_db('delete from Meals where email = (?) and date = (?) and start_time = (?)',
                 [current_user.email, request.form['date'], request.form['start_time']])
    elif table_id == "Social":
        query_db('delete from Social where email = (?) and date = (?) and start_time = (?)',
                 [current_user.email, request.form['date'], request.form['start_time']])
    elif table_id == "Downtime":
        query_db('delete from Downtime where email = (?) and date = (?) and start_time = (?)',
                 [current_user.email, request.form['date'], request.form['start_time']])
    print(table_id, current_user.email, request.form['date'], request.form['start_time'])
    print("deleted row")
    return 'OK'


@app.route('/add', methods=['POST'])
def add_entry():
    global current_user
    if not request.form:
        return
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    table_id = request.form['id']
    print(request.form['end_time'])
    if table_id == "Mood":
        query_db('insert into Mood (email, date, happiness) values(?,?,?)',
                 [current_user.email, request.form['date'], request.form['happiness']])
    elif table_id == "Sleep":
        query_db('insert into Sleep (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
    elif table_id == "Exercise":
        query_db('insert into Exercise (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
    elif table_id == "Work":
        query_db('insert into Work (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
        print(request.form['start_time'])
        print(request.form['end_time'])
    elif table_id == "Meals":
        query_db('insert into Meals (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
    elif table_id == "Social":
        query_db('insert into Social (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
    elif table_id == "Downtime":
        query_db('insert into Downtime (email, date, start_time, end_time, quality) values(?,?,?,?,?)',
                 [current_user.email, request.form['date'], request.form['start_time'], request.form['end_time'], request.form['quality']])
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    flash('New mood was successfully posted.')
    return 'OK'


@app.route('/calendar')
def show_cal():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    mood = query_db('select date, happiness from Mood where email = (?) order by date desc', [current_user.email])
    db = get_db()
    # db.row_factory = dict_factory
    # cur.execute('select date, happiness from Mood where email = (?) order by date desc', [current_user.email])
    # r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    # cur.connection.close()
    # print(r[0] if r else None)
    # mood = r[0] if r else None
    # moods = [dict(zip([key[0] for key in cursor.description], row)) for row in mood]
    # print(json.dumps({'mood': moods}))
    return render_template('external-dragging-builtin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global current_user
    if session.get('logged_in') and current_user:
        return redirect(url_for('show_cal'))
    error = None
    if request.method == 'POST':
        if request.form['email'] not in query_db('select email from RegisteredUser'):
            query_db('insert into RegisteredUser (name, email, password) values(?,?,?)',
                     [request.form['name'], request.form['email'], request.form['password']])
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
        passwordQuery = query_db('select password from RegisteredUser where email = ?', [request.form['email']])
        if passwordQuery is None:
            passwordQuery = []
        p = [x['password'] for x in passwordQuery]
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
            return redirect(url_for('show_cal'))
    return render_template('login.html', error=error)


@app.route('/monthlytrends')
def monthly():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    return render_template('monthly.html')


@app.route('/weeklytrends')
def weekly():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    return render_template('weekly.html')


@app.route('/dailytrends')
def daily():
    global current_user
    if not session.get('logged_in') or not current_user:
        return redirect(url_for('login'))
    return render_template('daily.html')


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
