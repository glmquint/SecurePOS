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
            self.connection = sqlite3.connect(f'../../db/{self.name}.db', check_same_thread=False)
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({self.tableName})")
            self.columns = [column[1] for column in cursor.fetchall()][1:]  # [1:] to remove the id column
        except sqlite3.Error as e:
            print("error from " + self.name + ".db:")
            print(e)

    def insert(self, row: list):
        cursor = self.connection.cursor()
        columns = ' ,'.join(self.columns)
        lenght = len(self.columns)
        insert_query = 'INSERT INTO ' + self.tableName + '(' + ' ,'.join(self.columns) + ') VALUES (' + ', '.join(
            '?' * len(self.columns)) + ')'

        #insert_query = 'INSERT INTO ' + self.tableName + '(' + str(columns) + ') VALUES (' + ', '.join(
            #'?' * lenght) + ')'
        cursor.executemany(
                insert_query,
                row)
        self.connection.commit()

    def remove(self, number = 0):
        cursor = self.connection.cursor()
        if number <= 0:
            cursor.execute('DELETE FROM ' + self.tableName)
        else:
            cursor.execute('Delete '
                           'from '+self.tableName+' where id IN ('
                           'Select id'
                           'from ' + self.tableName+
                           ' limit '+ number+' );'
                           )
        self.connection.commit()

    def retrieve(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM ' + self.tableName)
        return cursor.fetchall()
