import sqlite3


class DBConnector:
    name = None
    columns = None
    connection: sqlite3.Connection = None
    tableName = None

    def __init__(self, dbConfig):
        self.name = dbConfig.name
        self.columns = dbConfig.columns
        self.tableName = dbConfig.tableName

        try:
            self.connection = sqlite3.connect(f'../../db/{self.name}.db')
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
        cursor.execute('SELECT * FROM ' + self.tableName)
        return cursor.fetchall()
