import sqlite3
from sqlite3 import Error

"""class to make a connection to a clutterbase and execute commands, it allows the use of Context managers
"""

class ClutterBaseConnection :
    """
        Parameters :
            name : str the name of the database to connect to
    """
    def __init__(self,name : str) :
        self.name=name
        self.connection=None

    def open(self) :
        try :
            self.connection=sqlite3.connect(self.name)
        except Error as e:
            print(f"error {e} with database {self.name}")

    def close(self) :
        self.connection.close()

    def __enter__(self) :
        self.open()
        return self

    def __exit__(self,exc_type, exc_value, exc_tb) :
        self.close()

    def _loadBlob(self,filename : str) :
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def add_item(self,name : str, description : str , mesh : str, top_image : str,side_image : str, front_image : str, persp_image : str) :
        meshType="obj"
        if mesh.endswith(".usd") :
            meshType="usd"
        elif mesh.endswith(".fbx") :
            meshType="fbx"


        cursor=  self.connection.cursor()
        query = """ INSERT INTO ClutterBase
                                  ( Name, Description, MeshData,TopImage,PerspImage,SideImage,FrontImage,FileType) VALUES (?,?,?,?,?,?,?,?)"""
        mesh_blob=self._loadBlob(mesh)
        top_image_blob=self._loadBlob(top_image)
        persp_image_blob=self._loadBlob(persp_image)
        side_image_blob=self._loadBlob(side_image)
        front_image_blob=self._loadBlob(front_image)
        
        query_data = (name,description,mesh_blob,top_image_blob,persp_image_blob,side_image_blob,front_image_blob,meshType)
        cursor.execute(query, query_data)
        self.connection.commit()
        cursor.close()

    def extract_mesh(self,name : str, out_name : str) :
        cursor=  self.connection.cursor()
        query="""SELECT MeshData,FileType FROM ClutterBase WHERE Name = ?;"""
        cursor.execute(query, [name])
        record = cursor.fetchone()
        if record !=None :
            if not out_name.endswith(record[1]) :
                out_name=f"{out_name}.{record[1]}"
            with open(out_name, 'wb') as file:
                file.write(record[0])
                
        cursor.close()
