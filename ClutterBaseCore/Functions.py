import sqlite3
from sqlite3 import Error

"""generate a new ClutterBase db file and generate the tables

    Parameters
    ----------
    file : str
        the file to generate for the databse, a full path can be passed as well as the name.        

        Returns
        -------
            bool
                True if database file can be created.
"""
def create_new_database(path : str)  ->bool :
    try :
        with sqlite3.connect(path) as connection :
            create_table_sql="""
            CREATE TABLE IF NOT EXISTS ClutterBase (
                id integer PRIMARY KEY AUTOINCREMENT,
                Name text NOT NULL,
                Description text Not Null,
                MeshData BLOB Not Null,
                TopImage BLOB NOT NULL,
                PerspImage BLOB NOT NULL,
                SideImage BLOB NOT NULL,
                FrontImage BLOB NOT NULL
                );
            """
            
            cursor=connection.cursor()
            cursor.execute(create_table_sql)
            return True
    except Error as e:
        print(e)
        return False
