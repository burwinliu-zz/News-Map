import webpage.data.python_scripts.database as db


class SystemDatabase(db.Database):
    def __init__(self):
        """
        init the system database -- already in system, just creating relational object to "talk about this system
        """
        column_names = tuple(("index", "schema", "name", "types", "columns"))
        types = tuple((int, str, str, str, str))
        super().__init__("system", "sys_info", column_names, types)

    def drop_table(self, name: str, schema: str):
        pass

    def check_table_exists(self, name: str, schema: str) -> bool:
        pass
