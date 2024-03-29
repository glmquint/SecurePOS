class DBConfig:
    """
        This class is responsible for managing the database configuration.
        It initializes the configuration with a database name and a table name.

        Attributes:
            database_name: The name of the database.
            table_name: The name of the table.

        Methods:
            None
    """
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name
