class DBConfig:
    name = None
    columns = None
    tableName = None

    def __init__(self, dbName, tableName, columns):
        self.name = dbName
        self.tableName = tableName
        self.columns = columns
