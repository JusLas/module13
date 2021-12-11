import sqlite3
from sqlite3 import Error

import click
from flask import current_app, g
from flask.cli import with_appcontext


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_connection():
    conn = getattr(g, '_database', None)

    if conn is None:
        conn = g._database = sqlite3.connect(current_app.config['DB_FILE'])
        conn.row_factory = dict_factory
    return conn


def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


@click.command('init-db')
@with_appcontext
def init_db():

    create_todos_sql = """
   -- todos table
   CREATE TABLE IF NOT EXISTS todos (
      id integer PRIMARY KEY,
      title text NOT NULL,
      description text,
      done BOOLEAN NOT NULL CHECK (done IN (0, 1))
   );
   """
    db = get_connection()

    if db is not None:
        execute_sql(db, create_todos_sql)


def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db)


def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


def insert(conn, table, **kwargs):
    """
    insert
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    values = tuple(v for v in kwargs.values())

    sql = f''' INSERT INTO {table}({", ".join(kwargs.keys())})
              VALUES({", ".join(['?'] * len(kwargs))})'''

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid


def update(conn, table, id, **kwargs):
    """
    update
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )

    sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(e)

    return False


def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(e)

    return False

def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")
