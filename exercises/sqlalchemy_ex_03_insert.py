from sqlalchemy_ex_02 import students, engine

ins = students.insert()

ins = students.insert().values(name='Eric', lastname='Idle')

conn = engine.connect()
result = conn.execute(ins)
conn.execute(ins, [
   {'name': 'John', 'lastname': 'Cleese'},
   {'name': 'Graham', 'lastname': 'Chapman'},
])
