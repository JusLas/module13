from sqlalchemy import create_engine, MetaData, Integer, String, Table, Column

engine = create_engine('sqlite:///database.db', echo=True)

meta = MetaData()

students = Table(
   'students', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

conn = engine.connect()
s = students.select().where(students.c.id > 2)
result = conn.execute(s)

for row in result:
   print(row)
