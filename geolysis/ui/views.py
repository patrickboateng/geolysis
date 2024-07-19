import pyqtgraph as pg
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QMainWindow,
    QMenu,
    QTableWidget,
    QTabWidget,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class LeftWiget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.tree_view = QTreeView()
        self.form_layout = QFormLayout()

        self.m_layout.addWidget(self.tree_view)
        self.m_layout.addLayout(self.form_layout)

        self.setLayout(self.m_layout)


class TopCenterWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.table_widget = QTableWidget()

        self.m_layout.addWidget(self.table_widget)

        self.setLayout(self.m_layout)


class BottomCenterWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        self.m_layout.addWidget(self.tab_widget)

        self.setLayout(self.m_layout)


class RightWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(True, True)
        self.plot_widget.setBackground("w")

        self.m_layout.addWidget(self.plot_widget)

        self.setLayout(self.m_layout)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("GeoLysis")

        self.m_widget = QWidget(self)
        self.left_widget = LeftWiget()
        self.top_center_widget = TopCenterWidget()
        self.bottom_center_widget = BottomCenterWidget()
        self.right_widget = RightWidget()

        self.m_layout = QGridLayout()

        self.menu_bar = self.menuBar()

        self.file_menu = QMenu(self.menu_bar)
        self.file_menu.setTitle("&File")

        self.menu_bar.addMenu(self.file_menu)

        self.tool_bar = QToolBar(self)
        self.tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(self.tool_bar)

        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        self.m_layout.addWidget(self.left_widget, 0, 0, 2, 2)
        self.m_layout.addWidget(self.top_center_widget, 0, 2, 1, 5)
        self.m_layout.addWidget(self.right_widget, 0, 7, 2, 5)
        self.m_layout.addWidget(self.bottom_center_widget, 1, 2, 1, 5)

        self.m_widget.setLayout(self.m_layout)
        self.setCentralWidget(self.m_widget)
