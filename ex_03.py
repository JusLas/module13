import sqlite3

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except sqlite3.Error as e:
       print(e)
   return conn

def add_projekt(conn, projekt):
   """
   Create a new projekt into the projects table
   :param conn:
   :param projekt:
   :return: projekt id
   """
   sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, projekt)
   conn.commit()
   return cur.lastrowid

def add_zadanie(conn, zadanie):
   """
   Create a new zadanie into the tasks table
   :param conn:
   :param zadanie:
   :return: zadanie id
   """
   sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, zadanie)
   conn.commit()
   return cur.lastrowid

if __name__ == "__main__":
   projekt = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")

   conn = create_connection("database.db")
   pr_id = add_projekt(conn, projekt)

   zadanie = (
       pr_id,
       "Czasowniki regularne",
       "Zapamiętaj czasowniki ze strony 30",
       "started",
       "2020-05-11 12:00:00",
       "2020-05-11 15:00:00"
   )

   zadanie_id = add_zadanie(conn, zadanie)

   print(pr_id, zadanie_id)
   conn.commit()
