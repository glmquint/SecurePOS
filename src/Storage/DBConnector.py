import sqlite3


class DBConnector:
    name = None
    connection: sqlite3.Connection = None
    tableName = None

    def __init__(self, dbConfig):
        self.name = dbConfig.database_name
        self.tableName = dbConfig.table_name

        try:
            self.connection = sqlite3.connect(f'../../db/{self.name}.db')
        except sqlite3.Error as e:
            print(e)

    def insert(self, row: list):
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.tableName})")
        column_names = [column[1] for column in cursor.fetchall()][0:]
        insert_query = 'INSERT INTO ' + self.tableName + '(' + ' ,'.join(column_names) + ') VALUES (' + ', '.join(
            '?' * len(column_names)) + ')'
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

    def count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM ' + self.tableName)
        return cursor.fetchall()

    def createTable(self):
        cursor = self.connection.cursor()
        cursor.execute(
            'CREATE TABLE PreparedSessions (MeanAbsoluteDifferencingTransactionTimestamps double, MeanAbsoluteDifferencingTransactionAmount double,MedianLongitude double,MedianLatitude double,MedianTargetIP double,MedianDestIP double,Label varchar(20))')
        self.connection.commit()

