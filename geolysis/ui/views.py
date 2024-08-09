import pyqtgraph as pg
from assets import resources_rc  # noqa: F401
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QTableView,
    QTableWidget,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from models import LabTestsModel

ICON_SIZE = QSize(16, 16)


# section_separator = QFrame()
# section_separator.setFrameShape(QFrame.HLine)
# section_separator.setFrameShadow(QFrame.Sunken)


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

        self.tab_widget = QTableWidget()

        self.m_layout.addWidget(self.tab_widget)

        self.setLayout(self.m_layout)


class CustomPlotWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.tab_widget = QTableWidget()

        self.m_layout.addWidget(self.tab_widget)

        self.setLayout(self.m_layout)


class GraphWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.plot = pg.PlotWidget()
        self.plot.showGrid(x=True, y=True, alpha=1)

        self.m_layout.addWidget(self.plot)

        self.setLayout(self.m_layout)


class GraphInfoWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_layout = QVBoxLayout()

        self.table_view = QTableView()

        self.m_layout.addWidget(self.table_view)

        self.setLayout(self.m_layout)


class GraphSettingsWidget(QWidget):
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

        self.init_ui()
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
        self.create_sidebar()

    def init_ui(self):
        self.m_widget = QWidget(self)

        self.data_entry = DataEntryWidget()
        self.plot_info = PlotInfoWidget()
        self.custom_plot = CustomPlotWidget()
        self.graph = GraphWidget()
        self.graph_info = GraphInfoWidget()
        self.graph_settings = GraphSettingsWidget()

        self.m_layout = QGridLayout()

        self.m_layout.addWidget(self.data_entry, 0, 0, 1, 6)
        self.m_layout.addWidget(self.plot_info, 1, 0, 1, 3)
        self.m_layout.addWidget(self.custom_plot, 1, 3, 1, 3)
        self.m_layout.addWidget(self.graph, 0, 6, 1, 6)
        self.m_layout.addWidget(self.graph_info, 1, 6, 1, 3)
        self.m_layout.addWidget(self.graph_settings, 1, 9, 1, 3)

        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)

        self.m_widget.setLayout(self.m_layout)
        self.setCentralWidget(self.m_widget)

    def create_actions(self):
        self.new = QAction(QIcon(":/icons/notebook.png"), "File", self)
        self.new.setStatusTip("Create a new file")

    def create_menus(self):
        self.menubar = self.menuBar()

        self.filemenu = QMenu(self.menubar)
        self.filemenu.setTitle("&File")

        self.menubar.addMenu(self.filemenu)
        self.filemenu.addAction(self.new)

    def create_toolbars(self):
        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.setIconSize(ICON_SIZE)
        self.toolbar.addAction(self.new)
        self.addToolBar(self.toolbar)

    def create_statusbar(self):
        self.statusbar = self.statusBar()
        self.setStatusBar(self.statusbar)

    def create_sidebar(self):
        sidebar = QDockWidget("Project Explorer", self)
        sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # sidebar.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget = QWidget(sidebar)

        self.tab_widget = QTabWidget(sidebar)
        self.tab_widget.setIconSize(ICON_SIZE)
        self.tab_widget.setDocumentMode(True)

        t_model = LabTestsModel()

        self.test_types = QListView()
        self.test_types.setModel(t_model)
        self.test_types.setEditTriggers(QListView.NoEditTriggers)

        self.test_types.setSpacing(2)

        self.tab_widget.addTab(
            self.test_types, QIcon(":/icons/jar-label.png"), "Test Type"
        )

        #: Sample Information
        sample_info_group_box = QGroupBox("Sample Information")
        self.sample_id = QLineEdit()
        self.sample_desc = QLineEdit()
        self.sample_depth = QLineEdit()

        self.sample_info_layout = QFormLayout()
        self.sample_info_layout.addRow(QLabel("Sample ID"), self.sample_id)
        self.sample_info_layout.addRow(
            QLabel("Sample Desc."), self.sample_desc
        )
        self.sample_info_layout.addRow(
            QLabel("Sample Depth"), self.sample_depth
        )
        sample_info_group_box.setLayout(self.sample_info_layout)

        # Sample Location
        sample_loc_group_box = QGroupBox("Sample Location")
        self.sample_loc_layout = QFormLayout()
        self.sample_loc_area_name = QLineEdit()

        rx = r"[+-]?\d+(\.\d+)?"
        validator = QRegularExpressionValidator(rx)

        self.latitude = QLineEdit()
        self.latitude.setValidator(validator)
        self.longitude = QLineEdit()
        self.longitude.setValidator(validator)
        self.sample_loc_layout.addRow(
            QLabel("Location Name"), self.sample_loc_area_name
        )
        self.sample_loc_layout.addRow(QLabel("Latitude"), self.latitude)
        self.sample_loc_layout.addRow(QLabel("Longitude"), self.longitude)
        sample_loc_group_box.setLayout(self.sample_loc_layout)

        #: Other Information
        other_info_group_box = QGroupBox("Other Information")
        self.ref_standard = QComboBox()
        self.ref_standard.addItems(["ASTM", "British Standard"])
        self.tested_by = QLineEdit()
        self.other_info_layout = QFormLayout()
        self.other_info_layout.addRow(
            QLabel("Ref. Standard"), self.ref_standard
        )
        self.other_info_layout.addRow(QLabel("Tested By"), self.tested_by)
        other_info_group_box.setLayout(self.other_info_layout)

        self.sidebar_layout.addWidget(self.tab_widget)
        self.sidebar_layout.addWidget(sample_info_group_box)
        self.sidebar_layout.addWidget(sample_loc_group_box)
        self.sidebar_layout.addWidget(other_info_group_box)

        self.sidebar_widget.setLayout(self.sidebar_layout)

        sidebar.setWidget(self.sidebar_widget)
        sidebar.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, sidebar)
