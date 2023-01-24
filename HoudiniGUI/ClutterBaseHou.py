import os
import sqlite3
import sys
import tempfile
from sqlite3 import Error

import hou
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtSql import (QSqlDatabase, QSqlQuery, QSqlQueryModel,
                           QSqlTableModel)


class ImageDataModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(ImageDataModel, self).__init__()
        self._data = data
        self.columns = ["Id       ", "Name      ", "Description     ", "Top","Side","Persp","Front","Format"]

    def headerData(self, section: int, orientation: Qt.Orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # return f"Column {section + 1}"
            return self.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return f"{section + 1}"




    def data(self, index,role):
        
        value=self._data[index.row()][index.column()]
        if role==Qt.CheckStateRole :
            return None
        # process images these are in columns 3,4,5,6 from our data
        if index.column() in [3, 4, 5, 6]:
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                return None
            if role == Qt.ItemDataRole.DecorationRole:
                variant = value
                # img = variant.toByteArray()
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(variant, "png")
                return pixmap
        else :
            return value
        

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])



class ClutterBaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the GUI components and layout
        self.setWindowTitle("ClutterBase")
        self.resize(800, 200)
        self.database=None
        # Create GridLayout
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.database_view = QtWidgets.QTableView(self)
        self.gridLayout.addWidget(self.database_view,0, 0, 1, 4)
        self.database_view.doubleClicked.connect(self.load_mesh)
        # add $HIP / $PROJECT Selection
        label=QtWidgets.QLabel("Mesh Destination")
        self.gridLayout.addWidget(label,1, 0, 1, 1)
        self.mesh_location=QtWidgets.QComboBox()
        self.mesh_location.addItems(["$HIP","$PROJECT"])
        self.gridLayout.addWidget(self.mesh_location,1, 1, 1, 1)
        self.mesh_path=QtWidgets.QComboBox()
        self.mesh_path.addItems(["/obj","/stage"])
        self.gridLayout.addWidget(self.mesh_path,1, 2, 1, 1)
        spacer = QtWidgets.QSpacerItem(40, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer,1, 3,)

        self.load_db = hou.qt.FileChooserButton()
        self.load_db.setFileChooserTitle("Please select a file")
        self.load_db.setFileChooserMode(hou.fileChooserMode.Read)
        self.load_db.fileSelected.connect(self.load_database)
        self.gridLayout.addWidget(self.load_db,1, 3, 1, 1)
        
        
    def load_mesh(self,index) :
        model = self.database_view.model()
        mesh_id=model.data(model.index(index.row(), 0),0)
        cursor=self.database.cursor()
        cursor.execute(f"SELECT MeshData,FileType,Name FROM ClutterBase WHERE Id = {mesh_id}; ")
        result=cursor.fetchone()
        mesh_data=result[0]
        mesh_type=result[1]
        hip_dir=hou.text.expandString("$HIP")
        out_name=f"{hip_dir}/mesh.{mesh_type}"
        with open(out_name, 'wb') as file:
            file.write(mesh_data)
        name=result[2].replace(" ","_")
        print(f"name is {result[2]}")
        geo_node=hou.node('/obj').createNode("geo")
        geo_node.setName(name)
        file_node=geo_node.createNode("file")
        file_node.parm("file").set(out_name)

        
 
    def load_database(self,filepath):

        """This does all the work"""
        # Get the folder to save to

        if filepath !=None :
            try :
                self.database=sqlite3.connect(filepath)
                cursor=self.database.cursor()
                cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
                tables=cursor.fetchall()
                print(f"got {tables}") 
                cursor.close()
                if not "ClutterBase" in tables[1] : 
                    hou.ui.displayMessage(f"Not a valid clutterbase file {filepath} {tables}")
                    return
                
                else :            
                    query ="""select id,Name,Description,TopImage,PerspImage,SideImage,FrontImage,FileType from ClutterBase;"""
                    cursor=self.database.cursor()
                    cursor.execute(query)
                    items=cursor.fetchall()
                    self.model=ImageDataModel(items)
                    self.database_view.setModel(self.model)                    
                    cursor.close() 
                    self.database_view.resizeRowsToContents()
                    self.database_view.resizeColumnsToContents()


            except Error as e:
                    print(f"error {e} with database {filepath}")




dialog = ClutterBaseDialog()
dialog.show()