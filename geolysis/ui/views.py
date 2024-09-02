import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import (
    NavigationToolbar2QT as NavigationToolbar,  # type: ignore
)
from matplotlib.figure import Figure
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QRegularExpressionValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMenu,
    QSplitter,
    QTableView,
    QTableWidget,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from geolysis.ui.assets import resources_rc  # noqa: F401
from geolysis.ui.models import CodeBook, LabTest, LabTestModel

matplotlib.use("QtAgg")

ICON_SIZE = QSize(20, 20)
# Maximum and minimum width of sidebar is
# 20% and 17% respectively.
SIDEBAR_MAX_SIZE = 0.2
SIDEBAR_MIN_SIZE = 0.15


# section_separator = QFrame()
# section_separator.setFrameShape(QFrame.HLine)
# section_separator.setFrameShadow(QFrame.Sunken)


class DataEntryWidget(QTableWidget):
    def __init__(self, parent, labtest: LabTest | None = None):
        super().__init__(parent)

        self.labtest = labtest

        if self.labtest is None:
            self.setRowCount(20)
            self.setColumnCount(20)


class PlotInfoWidget(QTableView):
    def __init__(self, parent):
        super().__init__(parent)


class CustomPlotWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)


# TODO: New design


class GraphWidget(FigureCanvasQTAgg):
    def __init__(self, figure=None) -> None:
        super().__init__(figure)


class CustomLineEdit(QLineEdit):
    def __init__(self, parent, rx: str | None = None):
        super().__init__(parent)

        if rx:
            self.setValidator(QRegularExpressionValidator(rx))


class LabTestView(QListView):
    def __init__(self, parent):
        super().__init__(parent)
        labtest_model = LabTestModel()
        self.setModel(labtest_model)
        self.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self.setSpacing(2)


class SideBarTabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setIconSize(ICON_SIZE)
        self.setDocumentMode(True)

        self.labtest = LabTestView(self)
        self.addTab(self.labtest, "Lab Tests")


class SideBarDockWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__("Project Explorer", parent)
        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
        )
        # self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        # Tab
        self.sidebar_tab = SideBarTabWidget(self)

        # Form
        rx = r"[+-]?\d+(\.\d+)?"
        self.id = CustomLineEdit(self)
        self.sample_desc = CustomLineEdit(self)
        self.sample_depth = CustomLineEdit(self)
        self.location_name = CustomLineEdit(self)
        self.latitude = CustomLineEdit(self, rx=rx)
        self.longitude = CustomLineEdit(self, rx=rx)
        self.ref_standard = QComboBox(self)
        self.ref_standard.addItems(tuple(CodeBook))
        self.tested_by = CustomLineEdit(self)

        form = QFormLayout()
        form.addRow(QLabel("Sample ID"), self.id)
        form.addRow(QLabel("Sample Desc."), self.sample_desc)
        form.addRow(QLabel("Sample Depth"), self.sample_depth)
        form.addRow(QLabel("Location Name"), self.location_name)
        form.addRow(QLabel("Latitude"), self.latitude)
        form.addRow(QLabel("Longitude"), self.longitude)
        form.addRow(QLabel("Tested By"), self.tested_by)
        form.addRow(QLabel("Ref. Standard"), self.ref_standard)

        form_group = QGroupBox()
        form_group.setLayout(form)

        v_mspl = QSplitter(Qt.Orientation.Vertical)
        v_mspl.addWidget(self.sidebar_tab)
        v_mspl.addWidget(form_group)
        v_mspl.setStretchFactor(0, 1)

        m_wgt = QWidget(self)
        v_box_mly = QVBoxLayout(m_wgt)
        v_box_mly.addWidget(v_mspl, stretch=1)
        m_wgt.setLayout(v_box_mly)

        self.setWidget(m_wgt)
        self.setFloating(False)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("GeoLysis")

        self.init_ui()
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
        self.create_sidebar()

    def resizeEvent(self, event):
        self.sidebar.setMaximumWidth(int(self.width() * SIDEBAR_MAX_SIZE))
        self.sidebar.setMinimumWidth(int(self.width() * SIDEBAR_MIN_SIZE))
        super().resizeEvent(event)

    def init_ui(self):
        m_wgt = QWidget(self)

        self.data_entry = DataEntryWidget(m_wgt)
        self.plot_info = PlotInfoWidget(m_wgt)
        self.custom_plot = CustomPlotWidget(m_wgt)

        fig = Figure(figsize=(5, 3))
        self.graph = GraphWidget(fig)
        self.graph_toolbar = NavigationToolbar(self.graph, self)

        h_box_wgt = QWidget(m_wgt)
        h_box_ly = QHBoxLayout(h_box_wgt)
        h_box_ly.addWidget(self.plot_info)
        h_box_ly.addWidget(self.custom_plot)
        h_box_ly.setContentsMargins(0, 0, 0, 0)
        h_box_wgt.setLayout(h_box_ly)

        v_spl = QSplitter(Qt.Orientation.Vertical)
        v_spl.addWidget(self.data_entry)
        v_spl.addWidget(h_box_wgt)
        v_spl.setStretchFactor(0, 1)

        h_mspl = QSplitter(Qt.Orientation.Horizontal)
        h_mspl.addWidget(v_spl)
        h_mspl.addWidget(self.graph)

        v_box_mly = QVBoxLayout(m_wgt)
        v_box_mly.addWidget(h_mspl)

        m_wgt.setLayout(v_box_mly)
        self.setCentralWidget(m_wgt)

    def create_actions(self):
        self.new_action = QAction(QIcon(":/icons/notebook.png"), "File", self)
        self.new_action.setStatusTip("Create a new file")

    def create_menus(self):
        self.menubar = self.menuBar()

        self.filemenu = QMenu(self.menubar)
        self.filemenu.setTitle("&File")

        self.menubar.addMenu(self.filemenu)
        self.filemenu.addAction(self.new_action)

    def create_toolbars(self):
        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.setIconSize(ICON_SIZE)
        self.toolbar.addAction(self.new_action)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.graph_toolbar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

    def create_statusbar(self):
        self.statusbar = self.statusBar()
        self.setStatusBar(self.statusbar)

    def create_sidebar(self):
        self.sidebar = SideBarDockWidget(self)
        self.sidebar.setMaximumWidth(200)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)
