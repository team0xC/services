import os
import sqlite3
from flask import Flask, request, g

application = Flask(__name__)

DATABASE = '../rw/database.db'
PASSWORD = 'changeme'
DEBUG = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kids'")
        res = cur.fetchone()
        print(res)
        if not res:
            with application.app_context():
                with application.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()
    return db


@application.route("/init")
def init_db():
    password = request.args.get('password')
    if password != PASSWORD:
        return "Wrong password.\n"
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    with application.app_context():
        db = get_db()
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    return "Database created.\n"


@application.route("/dump/<table>")
def dump_db(table):
    password = request.args.get('password')
    if password != PASSWORD:
        return "Wrong password.\n"
    if not DEBUG:
        return "Not in debug mode.\n"
    cur = get_db().cursor()
    cur.execute('SELECT * from %s' % table)
    rows = cur.fetchall()
    res = ""
    for row in rows:
        res = res + str(row) + "\n"
    return res


@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@application.route("/")
def hello():
    return "Kid finder service.\n"


@application.route("/kid")
def add_kid():
    # Creates a kid
    try:
        first = request.args.get('first')
        last = request.args.get('last')
        age = request.args.get('age')
    except Exception as e:
        print(str(e))
        return "Malformed request.\n"
    try:
        db = get_db()
        cur = db.cursor()
        sql = '''INSERT INTO kids(first,last,age) VALUES(?,?,?)'''
        cur.execute(sql, (first, last, age))
    except Exception as e:
        print(str(e))
        return "Query failed.\n"
    db.commit()
    return "Created kid %d\n" % cur.lastrowid


@application.route("/party")
def add_party():
    # Creates the party
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        description = request.args.get('description')
        invitation = request.args.get('invitation')
    except Exception as e:
        print(str(e))
        return "Malformed request.\n"
    try:
        db = get_db()
        cur = db.cursor()
        sql = '''INSERT INTO parties(start_time,end_time,description,invitation) VALUES(?,?,?,?)'''
        cur.execute(sql, (start, end, description, invitation))
    except Exception as e:
        print(str(e))
        return "Query failed.\n"
    db.commit()
    return "Created party %d\n" % cur.lastrowid


@application.route("/attend")
def add_kid_to_party():
    # Adds a kid to the party
    try:
        kid_id = request.args.get('kid')
        party_id = request.args.get('party')
    except Exception as e:
        print(str(e))
        return "Malformed request.\n"
    try:
        db = get_db()
        cur = db.cursor()
        sql = '''SELECT first,last FROM kids WHERE id=?'''
        cur.execute(sql, (kid_id,))
        res = cur.fetchone()
        # print res
        if not res:
            return "No such kid.\n"
        first = res[0]
        last = res[1]

        sql = '''SELECT kid_list FROM parties WHERE id=?'''
        cur.execute(sql, (party_id,))
        res = cur.fetchone()
        if not res:
            return "No such party.\n"
        kid_list = res[0]
        # print res
        kid_str = "%s_%s" % (first, last)

        if not kid_list:
            kid_list = kid_str
        else:
            if kid_str in kid_list:
                return "Kid already at party.\n"

            kid_list = kid_list + ',' + kid_str

        sql = '''UPDATE parties SET kid_list=? WHERE id=?'''
        cur.execute(sql, (kid_list, party_id))
    except Exception as e:
        print(str(e))
        return "Query failed.\n"
    db.commit()
    return "Added kid %s to party %s\n" % (kid_id, party_id)


@application.route("/find")
def get_party():
    # Returns the parties where the kid is
    try:
        kid_id = int(request.args.get('kid'))
    except Exception as e:
        print(str(e))
        return "Malformed request.\n"
    try:
        db = get_db()
        cur = db.cursor()
        sql = '''SELECT first,last FROM kids WHERE id=?'''
        cur.execute(sql, (kid_id,))
        res = cur.fetchone()
        # print res
        if not res:
            return "No such kid.\n"

        first = res[0]
        last = res[1]
        kid_str = "%s_%s" % (first, last)

        sql = '''SELECT id  FROM parties WHERE kid_list LIKE '%%%s%%' ''' % kid_str
        print("EXECUTING: [%s]" % sql)
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows:
            return "No party with this kid.\n"
        print(rows)
        party_ids = ""
        for row in rows:
            party_id = row[0]
            if not party_ids:
                party_ids = str(party_id)
            else:
                party_ids = party_ids + "," + str(party_id)
    except Exception as e:
        print(str(e))
        return "Query failed.\n"
    return "Found kid at these parties: %s" % party_ids


@application.route("/info")
def get_party_info():
    # Creates the party
    try:
        id = int(request.args.get('id'))
        invitation = request.args.get('invitation')
    except Exception as e:
        print(str(e))
        return "Malformed request.\n"
    try:
        db = get_db()
        cur = db.cursor()
        sql = '''SELECT description,start_time,end_time,kid_list FROM parties WHERE invitation=? and id=?'''
        cur.execute(sql, (invitation, id))
    except Exception as e:
        print(str(e))
        return "Query failed.\n"

    res = cur.fetchone()
    if not res:
        return "No such party.\n"

    return "Party [%s] from %s to %s with %s\n" % (res)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
