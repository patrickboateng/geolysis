import pyqtgraph as pg
from assets import resources_rc  # noqa: F401
from PySide6.QtCore import QSize, QStringListModel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QTableView,
    QTableWidget,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class SideBarWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        model = QStringListModel()
        model.setStringList(["Particle Size Distribution", "Atterberg Limits"])
        # Add data to the model

        self.tree_view = QListView()
        self.tree_view.setModel(model)

        wgt = QWidget()
        lay = QVBoxLayout()
        lay.addWidget(self.tree_view)
        wgt.setLayout(lay)

        self.tab_widget.addTab(wgt, QIcon(":/icons/beaker.png"), "Tests")

        self.m_layout.addWidget(self.tab_widget)

        self.setLayout(self.m_layout)


class SampleInfoWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        #: Sample Information
        self.sample_id = QLineEdit()
        self.sample_desc = QTextEdit()
        self.sample_depth = QLineEdit()
        self.ref_standard = QComboBox()
        self.ref_standard.addItems(["ASTM", "BS"])
        self.location = QLineEdit()

        #: Other Information
        self.tested_by = QLineEdit()

        # section_separator = QFrame()
        # section_separator.setFrameShape(QFrame.HLine)
        # section_separator.setFrameShadow(QFrame.Sunken)

        self.form_layout = QFormLayout()
        self.form_layout.addRow(QLabel("Sample ID"), self.sample_id)
        self.form_layout.addRow(QLabel("Sample Desc."), self.sample_desc)
        self.form_layout.addRow(QLabel("Sample Depth"), self.sample_depth)
        self.form_layout.addRow(QLabel("Ref. Standard"), self.ref_standard)
        self.form_layout.addRow(QLabel("Location"), self.location)

        self.form_layout.addRow(QLabel("Tested By"), self.tested_by)

        self.m_layout.addLayout(self.form_layout)

        self.setLayout(self.m_layout)


class DataEntryWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.table_widget = QTableWidget()

        self.m_layout.addWidget(self.table_widget)

        self.setLayout(self.m_layout)


class PlotInfoWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        self.m_layout.addWidget(self.tab_widget)

        self.setLayout(self.m_layout)


class GraphWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True, alpha=1)

        self.m_layout.addWidget(self.plot_widget)

        self.setLayout(self.m_layout)


class GraphInfoWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.table_view = QTableView()

        self.m_layout.addWidget(self.table_view)

        self.setLayout(self.m_layout)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("GeoLysis")

        self.m_widget = QWidget(self)

        self.sidebar = SideBarWidget()
        self.sample_info = SampleInfoWidget()
        self.data_entry = DataEntryWidget()
        self.plot_info = PlotInfoWidget()
        self.graph = GraphWidget()
        self.graph_info = GraphInfoWidget()

        self.m_layout = QGridLayout()

        self.menu_bar = self.menuBar()

        self.file_menu = QMenu(self.menu_bar)
        self.file_menu.setTitle("&File")

        self.menu_bar.addMenu(self.file_menu)

        self.tool_bar = QToolBar("Main toolbar")
        self.tool_bar.setIconSize(QSize(16, 16))
        # self.tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        new = QAction(QIcon(":/icons/notebook.png"), "File", self)
        # new.setStatusTip("Create a new file")
        # self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.tool_bar.addAction(new)
        self.addToolBar(self.tool_bar)

        self.file_menu.addAction(new)

        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        self.m_layout.addWidget(self.sidebar, 0, 0, 1, 2)
        self.m_layout.addWidget(self.sample_info, 1, 0, 1, 2)
        self.m_layout.addWidget(self.data_entry, 0, 2, 1, 5)
        self.m_layout.addWidget(self.plot_info, 1, 2, 1, 5)
        self.m_layout.addWidget(self.graph, 0, 7, 1, 5)
        self.m_layout.addWidget(self.graph_info, 1, 7, 1, 5)

        self.m_widget.setLayout(self.m_layout)
        self.setCentralWidget(self.m_widget)
