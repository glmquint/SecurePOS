import os
import sqlite3
from threading import RLock


class DBConnector:
    """
        This class is responsible for managing the connection to a SQLite database.
        It initializes the connection with a database name and a table name, and provides methods
        for various database operations such as insert, remove, retrieve, and count.

        Attributes:
            name: The name of the database.
            connection: The SQLite connection object.
            tableName: The name of the table.
            columns: A list of column names in the table.
            lock: A reentrant lock to ensure thread safety during database operations.

        Methods:
            insert: Inserts a row into the table.
            remove: Removes all rows from the table.
            remove_n: Removes a specified number of rows from the table.
            retrieve_n: Retrieves a specified number of rows from the table.
            retrieve: Retrieves all rows from the table.
            count: Counts the number of rows in the table.
            delete_by_column: Deletes rows where a specified column has a specified value.
            retrieve_by_column: Retrieves rows where a specified column has a specified value.
            isNumberOfRecordsSufficient: Checks if the number of distinct systems in the records is sufficient.
            retrieve_joined_labels: Retrieves a specified number of rows from a join of the labels and security_labels.
            remove_joined_labels: Removes a specified number of rows from a join of the labels and security_labels.
    """
    name: str = None
    connection: sqlite3.Connection = None
    tableName: str = None
    columns: [str] = None
    lock = RLock = RLock()

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.tableName = kwargs.get('table_name', '')

        try:
            self.connection = sqlite3.connect(
                f'{os.path.dirname(__file__)}/../../db/{self.name}.db',
                check_same_thread=False)
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({self.tableName})")
            # [1:] to remove the id column
            self.columns = [column[1] for column in cursor.fetchall()][1:]
        except sqlite3.Error as e:
            print(e, __file__)
            raise Exception(e)

    def insert(self, row: list):
        with self.lock:
            cursor = self.connection.cursor()
            insert_query = 'INSERT INTO ' + self.tableName + \
                '(' + ' ,'.join(self.columns) + ') VALUES (' + ', '.join('?' * len(self.columns)) + ')'
            cursor.executemany(
                insert_query,
                row)
            self.connection.commit()

    def remove(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM ' + self.tableName)
            self.connection.commit()

    def remove_n(self, number: int):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                'DELETE FROM ' +
                self.tableName +
                ' WHERE rowid IN ( select rowid from ' +
                self.tableName +
                ' order by rowid limit ' +
                str(number) +
                ')')
            self.connection.commit()

    def retrieve_n(self, number: int):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT ' +
                ' ,'.join(
                    self.columns) +
                ' FROM ' +
                self.tableName +
                ' order by rowid limit ' +
                str(number))
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def retrieve(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT ' +
                ' ,'.join(
                    self.columns) +
                ' FROM ' +
                self.tableName)
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def count(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM ' + self.tableName)
            return cursor.fetchall()[0][0]

    def delete_by_column(self, column, value):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                f'DELETE FROM {self.tableName} WHERE {column} = ?', (value,))
            self.connection.commit()

    def retrieve_by_column(self, param, value):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                f'SELECT {" ,".join(self.columns)} FROM {self.tableName} WHERE {param} = ?',
                (value,
                 ))
            return [dict(zip(self.columns, x)) for x in cursor.fetchall()]

    def isNumberOfRecordsSufficient(self):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                "select uuid, count(distinct(objtype)) as different_systems from record group by uuid order by different_systems desc limit 1;")
            return cursor.fetchall()

    def retrieve_joined_labels(self, number):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                "select* from labels as l  inner join security_labels as sl  on l.uuid == sl.uuid limit " +
                str(number) +
                ";")
            return cursor.fetchall()

    def remove_joined_labels(self, number):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(
                "delete from labels where uuid in (select l.uuid from labels as l inner join security_labels as sl on l.uuid=sl.uuid limit " +
                str(number) +
                ");")
            self.connection.commit()
