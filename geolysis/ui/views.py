import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QTableView,
    QToolBar,
    QTreeView,
    QWidget,
)


class DataEntry(QTableView):
    pass


class LeftSideBar(QTreeView):
    pass


class RightSideBar:
    pass


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("GeoLysis")
        # self.setToolButtonStyle(Qt.ToolButtonTextOnly)

        new = QAction("New", self)
        new.setStatusTip("Create a file")

        self.menu_bar = self.menuBar()

        self.file_menu = QMenu(self.menu_bar)
        self.file_menu.setTitle("&File")

        self.menu_bar.addMenu(self.file_menu)
        self.file_menu.addAction(new)

        self.tool_bar = QToolBar(self)
        self.tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(self.tool_bar)

        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
