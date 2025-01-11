from pypika import (
    Field as F,
    Query,
    Table,
    functions as fn,
)
from pypika.terms import *
from datetime import datetime


class Builder(object):
    def __init__(self, client_write, client_read) -> None:
        self.database_write = client_write
        self.database_read = client_read
        self.cursor_write = self.database_write.cursor()
        self.cursor_read = self.database_read.cursor()

    def write_client(self):
        return self.database_write
    
    def read_client(self):
        return self.database_read
    
    def set_table(self, table):
        self.table = Table(table)

    def table(self):
        return self.table
    
    def query(self):
        return Query().from_(self.table)

    def upsert(self, data):
        try:
            q = Query.into(self.table).columns(*data.keys()).insert(*data.values())
            for column, value in data.items():
                q = q.on_duplicate_key_update(self.table[column], Values(self.table[column]))
        except Exception as e:
            raise e
        else:
            self.cursor.execute(q.get_sql())
            self.database_write.commit()
            return  self.cursor.lastrowid
        
    def insert(self, data):
        try:
            q = Query.into(self.table).columns(*data.keys()).insert(*data.values())
        except Exception as e:
            raise e
        else:
            self.cursor_write.execute(q.get_sql())
            self.database_write.commit()
            return  self.cursor.lastrowid

    def exec(self, query):
        q = query.get_sql()
        try:
            self.cursor_read.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor_read
        
    def meta(self, q, limit, page):
        q = q.select(fn.Count('*').as_('total'))
        query = q.get_sql()
        try:
            self.cursor_read.execute(query)
        except Exception as e:
            raise e
        else:
            return {
                'total': self.cursor_read.fetchone()['total'],
                'page': page if page <= 0 else page,
                'limit': limit,
                'page_next': page+1
            }
        
    def fetch(self, query):
        q = query.get_sql()
        print(q)
        try:
            self.cursor_read.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor_read.fetchall()
        
    def fetch_row(self, query):
        q = query.get_sql()
        try:
            self.cursor_read.execute(q)
        except Exception as e:
            raise e
        else:
            return self.cursor_read.fetchone()
        
    def delete(self, id):
        q = Query.update(self.table).set('deleted_at', datetime.now()).where(self.table.id == id)
        try:
            self.cursor_write.execute(q.get_sql())
        except Exception as e:
            raise e
        else:
            return True