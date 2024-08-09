from enum import StrEnum
from typing import Sequence

from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QColor


class LabTest(StrEnum):
    ATTERBERG_LIMITS = "AL"
    COMPACTION = "CP"
    PARTICLE_SIZE_DISTRIBUTION = "PSD"


TEST_TYPES = (
    LabTest.ATTERBERG_LIMITS,
    LabTest.COMPACTION,
    LabTest.PARTICLE_SIZE_DISTRIBUTION,
)


class LabTestsModel(QAbstractListModel):
    def __init__(self, labtests: Sequence[LabTest] = TEST_TYPES):
        super().__init__()

        self.labtests = labtests

    def data(self, index, role):
        row = index.row()
        test_type = self.labtests[row]

        if role == Qt.DisplayRole:
            return test_type.name.replace("_", " ")

        if role == Qt.DecorationRole:
            return QColor("blue")

        if role == Qt.StatusTipRole:
            return "Tip"

    def rowCount(self, index):
        return len(self.labtests)
