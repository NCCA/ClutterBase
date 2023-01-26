import os
import sys
import tempfile

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from shiboken2 import wrapInstance


def get_main_window():
    """this returns the maya main window for parenting"""
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QDialog)


class ImageDataModel(QSqlQueryModel):
    def __init__(self, parent=None):
        # super(QSqlQueryModel, self).__init__(parent)
        super().__init__(parent)

    def data(self, index, role=0):
        value = QSqlQueryModel.data(self, index, role)
        # process images these are in columns 3,4,5,6 from our data
        if index.column() in [3, 4, 5, 6]:
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                return None
            if role == Qt.ItemDataRole.DecorationRole:
                variant = QSqlQueryModel.data(self, index, Qt.ItemDataRole.DisplayRole)
                # img = variant.toByteArray()
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(variant, "png")
                return pixmap

        else:
            return value


class ClutterBaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window()):
        """init the class and setup dialog"""
        # Python 3 does inheritance differently to 2 so support both
        # as Maya 2020 is still Python 2
        if sys.version_info.major == 3:
            super().__init__(parent)
        # python 2
        else:
            super(ClutterBaseDialog, self).__init__(parent)
        # Set the GUI components and layout
        self.setWindowTitle("ClutterBase")
        self.resize(800, 200)
        self.database = None
        # Create GridLayout
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.database_view = QtWidgets.QTableView(self)
        self.gridLayout.addWidget(self.database_view, 0, 0, 1, 4)
        self.database_view.doubleClicked.connect(self.load_mesh)

        self.load_db = QtWidgets.QPushButton("Load Database", self)
        self.load_db.clicked.connect(self.load_database)
        self.gridLayout.addWidget(self.load_db, 1, 3, 1, 1)

    def load_mesh(self, index):
        model = self.database_view.model()
        mesh_id = model.data(model.index(index.row(), 0))

        query = """SELECT MeshData,FileType FROM ClutterBase WHERE Id = ?;"""
        query = QSqlQuery()
        result = query.exec_(
            f"SELECT MeshData,FileType FROM ClutterBase WHERE Id = {mesh_id}; "
        )
        if result:
            query.next()
            mesh_data = query.value(0)
            mesh_type = query.value(1)
            print(f"query worked {mesh_type=}")
            with tempfile.TemporaryDirectory() as tempdir:
                out_name = f"{tempdir}/mesh.{mesh_type}"
                with open(out_name, "wb") as file:
                    file.write(mesh_data)
                import_type = "OBJ"
                if mesh_type == "usd":
                    import_type = "USD Import"
                elif mesh_type == "fbx":
                    import_type = "FBX"

                cmds.file(
                    out_name,
                    gr=True,
                    i=True,
                    groupName="ClutterBaseImport",
                    type=import_type,
                )

        else:
            print("query error")

    def load_database(self):
        """This does all the work"""
        # Get the folder to save to
        name = cmds.fileDialog2(fm=1)
        if name != None:
            self.database = QSqlDatabase.addDatabase("QSQLITE")
            print(name[0])
            self.database.setDatabaseName(str(name[0]))
            self.connected = self.database.open()

            if not "ClutterBase" in self.database.tables():
                QtWidgets.QMessageBox.critical(
                    self,
                    "CRITICAL ERROR",
                    "Not a valid ClutterBase File",
                    QtWidgets.QMessageBox.StandardButton.Abort,
                )

            else:
                query = ImageDataModel()
                queryColumns = "id,Name ,Description ,TopImage ,PerspImage ,SideImage ,FrontImage ,FileType"
                query.setQuery(f"select {queryColumns} from ClutterBase")
                self.database_view.setModel(query)
                self.database_view.resizeRowsToContents()
                self.database_view.resizeColumnsToContents()


if __name__ == "__main__":

    # If we have a dialog open already close
    try:
        clutterbase_dialog.close()
        clutterbase_dialog.deleteLater()
    except:
        pass

    clutterbase_dialog = ClutterBaseDialog()
    clutterbase_dialog.show()
