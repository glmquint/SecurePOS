class DBConfig:
    database_name = None
    table_name = None

    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name


