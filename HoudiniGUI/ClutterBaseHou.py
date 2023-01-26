import os
import sqlite3
import sys
import tempfile
from pathlib import Path
from sqlite3 import Error

import hou
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel


class ImageDataModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(ImageDataModel, self).__init__()
        self._data = data
        self.columns = [
            "Id       ",
            "Name      ",
            "Description     ",
            "Top",
            "Side",
            "Persp",
            "Front",
            "Format",
        ]

    def headerData(self, section: int, orientation: Qt.Orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            # return f"Column {section + 1}"
            return self.columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.CheckStateRole:
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
        else:
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
        self.database = None
        # Create GridLayout
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.database_view = QtWidgets.QTableView(self)
        self.gridLayout.addWidget(self.database_view, 0, 0, 1, 5)
        self.database_view.doubleClicked.connect(self.load_mesh)
        # add $HIP / $PROJECT Selection
        label = QtWidgets.QLabel("Mesh Destination")
        self.gridLayout.addWidget(label, 1, 0, 1, 1)
        self.mesh_location = QtWidgets.QComboBox()
        self.mesh_location.addItems(["$HIP", "$PROJECT"])
        self.mesh_location.setItemData(0, "Store meshes in $HIP folder", Qt.ToolTipRole)
        self.mesh_location.setItemData(
            1, "Store meshes in $PROJECT folder", Qt.ToolTipRole
        )
        self.gridLayout.addWidget(self.mesh_location, 1, 1, 1, 1)
        self.mesh_folder = QtWidgets.QLineEdit("ClutterGeo")
        self.gridLayout.addWidget(self.mesh_folder, 1, 2, 1, 1)

        self.mesh_path = QtWidgets.QComboBox()
        self.mesh_path.addItems(["/obj", "/stage"])
        self.mesh_path.setItemData(0, "create geo in /obj", Qt.ToolTipRole)
        self.mesh_path.setItemData(1, "create geo in /stage", Qt.ToolTipRole)

        self.gridLayout.addWidget(self.mesh_path, 1, 3, 1, 1)

        self.load_db = hou.qt.FileChooserButton()
        self.load_db.setFileChooserTitle("Please select a file")
        self.load_db.setFileChooserMode(hou.fileChooserMode.Read)
        self.load_db.fileSelected.connect(self.load_database)
        self.gridLayout.addWidget(self.load_db, 1, 4, 1, 1)

    def _write_to_slash_stage(
        self, mesh_data: str, mesh_type: str, mesh_name: str
    ) -> None:
        if self.mesh_location.currentIndex() == 0:
            dir = hou.text.expandString("$HIP")
        else:
            dir = hou.text.expandString("$PROJECT")
        # check to see if folder exists and create if not
        Path(f"{dir}/{self.mesh_folder.text()}/{mesh_name}").mkdir(
            parents=True, exist_ok=True
        )

        out_name = (
            f"{dir}/{self.mesh_folder.text()}/{mesh_name}/{mesh_name}.{mesh_type}"
        )
        with open(out_name, "wb") as file:
            file.write(mesh_data)
        # if input is usd it's easy
        if mesh_type == "usd":
            file_node = hou.node("/stage").createNode("assetreference", mesh_name)
            hou_parm = file_node.parm("filepath")
            hou_parm.set(out_name)
        # Non USD need to be imported as sops
        else:
            # first copy to object level
            self._write_to_slash_obj(mesh_data, mesh_type, mesh_name)
            sop_import = hou.node("/stage").createNode("sopimport")
            # sop_import.name(f"{mesh_name}")
            path = sop_import.parm("soppath")
            path.set(f"/obj/{mesh_name}")

    def _write_to_slash_obj(
        self, mesh_data: str, mesh_type: str, mesh_name: str
    ) -> None:
        if self.mesh_location.currentIndex() == 0:
            dir = hou.text.expandString("$HIP")
        else:
            dir = hou.text.expandString("$PROJECT")
        # check to see if folder exists and create if not
        Path(f"{dir}/{self.mesh_folder.text()}/{mesh_name}").mkdir(
            parents=True, exist_ok=True
        )

        out_name = (
            f"{dir}/{self.mesh_folder.text()}/{mesh_name}/{mesh_name}.{mesh_type}"
        )
        with open(out_name, "wb") as file:
            file.write(mesh_data)
        geo_node = hou.node("/obj").createNode("geo")
        geo_node.setName(mesh_name)
        file_node = geo_node.createNode("file")
        file_node.parm("file").set(out_name)

    def load_mesh(self, index: int) -> None:
        model = self.database_view.model()
        mesh_id = model.data(model.index(index.row(), 0), 0)
        cursor = self.database.cursor()
        cursor.execute(
            f"SELECT MeshData,FileType,Name FROM ClutterBase WHERE Id = {mesh_id}; "
        )
        result = cursor.fetchone()
        mesh_data = result[0]
        mesh_type = result[1]
        # can have spaces in name field to replace with _
        mesh_name = result[2].replace(" ", "_")
        # see if we are working at object level or stage
        if self.mesh_path.currentIndex() == 0:  # /obj
            self._write_to_slash_obj(mesh_data, mesh_type, mesh_name)
        else:
            self._write_to_slash_stage(mesh_data, mesh_type, mesh_name)

    def get_absolute_filename(self, path: str) -> str:
        # so we got some data we need to split it as we could have $JOB $HIP or $HOME prepended
        # to it  if we partition based on the / we get a tuple with "", "/","/....." where the
        # first element is going to be an environment var etc.
        file = path.partition("/")
        # we have $HOME so extract the full $HOME path and use it
        if file[0] == "$HOME":
            prefix = str(hou.getenv("HOME"))
        elif file[0] == "$HIP":
            # we have $HIP so extract the full $HIP path
            prefix = str(hou.getenv("HIP"))
        # we have a $JOB so extract the full $JOB path
        elif file[0] == "$JOB":
            prefix = str(hou.getenv("JOB"))
        # nothing so just blank the string
        else:
            prefix = str("")
        # now construct our new file name from the elements we've found
        return f"{prefix}/{file[2]}"

    def load_database(self, filepath: str) -> None:

        """This does all the work"""
        # Get the folder to save to
        if filepath != "":
            try:
                filepath = self.get_absolute_filename(filepath)
                self.database = sqlite3.connect(filepath)
                cursor = self.database.cursor()
                cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
                tables = cursor.fetchall()
                print(f"got {tables}")
                cursor.close()
                if not "ClutterBase" in tables[1]:
                    hou.ui.displayMessage(
                        f"Not a valid clutterbase file {filepath} {tables}"
                    )
                    return

                else:
                    query = """select id,Name,Description,TopImage,PerspImage,SideImage,FrontImage,FileType from ClutterBase;"""
                    cursor = self.database.cursor()
                    cursor.execute(query)
                    items = cursor.fetchall()
                    self.model = ImageDataModel(items)
                    self.database_view.setModel(self.model)
                    cursor.close()
                    self.database_view.resizeRowsToContents()
                    self.database_view.resizeColumnsToContents()
            except Error as e:
                print(f"error {e} with database {filepath}")


dialog = ClutterBaseDialog()
dialog.show()
