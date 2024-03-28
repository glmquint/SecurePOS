import os
import sqlite3
from threading import RLock


class DBConnector:
    name       : str                = None
    connection : sqlite3.Connection = None
    tableName  : str                = None
    columns    : [str]              = None
    lock       = RLock              = RLock()

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.tableName = kwargs.get('table_name', '')

        try:
            self.connection = sqlite3.connect(f'{os.path.dirname(__file__)}/../../db/{self.name}.db', check_same_thread=False)
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({self.tableName})")
            self.columns = [column[1] for column in cursor.fetchall()][1:]  # [1:] to remove the id column
        except sqlite3.Error as e:
            print(e, __file__)
            raise Exception(e)

    def insert(self, row: list):
        with self.lock:
            cursor = self.connection.cursor()
            insert_query = 'INSERT INTO ' + self.tableName + '(' + ' ,'.join(self.columns) + ') VALUES (' + ', '.join(
                '?' * len(self.columns)) + ')'
            cursor.executemany(
                    insert_query,
                    row)
            self.connection.commit()

    def remove(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM ' + self.tableName)
            self.connection.commit()

    def remove_n(self,number:int):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM ' + self.tableName + ' WHERE rowid IN ( select rowid from ' + self.tableName + ' order by rowid limit '+str(number)+')')
            self.connection.commit()

    def retrieve_n(self,number:int):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('SELECT ' + ' ,'.join(self.columns) + ' FROM '+ self.tableName + ' order by rowid limit ' + str(number))
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def retrieve(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('SELECT ' + ' ,'.join(self.columns) + ' FROM ' + self.tableName)
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def count(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM ' + self.tableName)
            return cursor.fetchall()[0][0]

    def delete_by_column(self, column, value):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(f'DELETE FROM {self.tableName} WHERE {column} = ?', (value,))
            self.connection.commit()

    def retrieve_by_column(self, param, value):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT {" ,".join(self.columns)} FROM {self.tableName} WHERE {param} = ?', (value,))
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def isNumberOfRecordsSufficient(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute("select uuid, count(distinct(objtype)) as different_systems from record group by uuid order by different_systems desc limit 1;")
            return cursor.fetchall()


    def retrieve_n_labels(self,number):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute("select* from labels as l  inner join security_labels as sl  on l.uuid == sl.uuid;")
            return cursor.fetchall()