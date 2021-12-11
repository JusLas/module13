import json
from db import utils as db_utils


class Todos:

    table = 'todos'

    def __init__(self):
        self.conn = db_utils.get_connection()

    def all(self):
        return db_utils.select_all(self.conn, self.table)

    def get(self, id):
        return db_utils.select_where(self.conn, self.table, id=id)

    def create(self, data):
        return db_utils.insert(self.conn, self.table, **data)

    def update(self, id, data):
        updated = db_utils.update(self.conn, self.table,  id, **data)
        return updated

    def delete(self, id):
        deleted = db_utils.delete_where(self.conn, self.table,  id=id)
        return deleted
