import sqlite3


class DBConnector:
    name                           = None
    connection: sqlite3.Connection = None
    tableName                      = None
    columns                        = None

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.tableName = kwargs.get('table_name', '')

        try:
            self.connection = sqlite3.connect(f'../../db/{self.name}.db', check_same_thread=False)
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({self.tableName})")
            self.columns = [column[1] for column in cursor.fetchall()][1:]  # [1:] to remove the id column
        except sqlite3.Error as e:
            print(e)

    def insert(self, row: list):
        cursor = self.connection.cursor()
        insert_query = 'INSERT INTO ' + self.tableName + '(' + ' ,'.join(self.columns) + ') VALUES (' + ', '.join(
            '?' * len(self.columns)) + ')'
        cursor.executemany(
            insert_query,
            row)
        self.connection.commit()

    def remove(self):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM ' + self.tableName)
        self.connection.commit()

    def retrieve(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT ' + ' ,'.join(self.columns) + ' FROM ' + self.tableName)
        return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM ' + self.tableName)
        return cursor.fetchall()[0][0]

    def delete_by_column(self, column, value):
        cursor = self.connection.cursor()
        cursor.execute(f'DELETE FROM {self.tableName} WHERE {column} = ?', (value,))
        self.connection.commit()

    def retrieve_by_column(self, param, value):
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT {" ,".join(self.columns)} FROM {self.tableName} WHERE {param} = ?', (value,))
        return [dict(zip(self.columns, x)) for x in cursor.fetchall()]
