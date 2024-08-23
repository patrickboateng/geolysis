from enum import StrEnum, unique

from PySide6.QtCore import QAbstractListModel, Qt


@unique
class CodeBook(StrEnum):
    ASTM = "ASTM"
    BRITISH_STANDARD = "BS"


@unique
class LabTest(StrEnum):
    ATTERBERG_LIMITS = "Atterberg Limits"
    STANDARD_COMPACTION = "Standard Compaction"
    MODIFIED_COMPACTION = "Modified Compaction"
    PARTICLE_SIZE_DISTRIBUTION = "Particle Size Distribution"


class LabTestModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

        self._labtests = tuple(LabTest)

    def data(self, index, role):
        row = index.row()
        test_type = self._labtests[row]

        if role == Qt.ItemDataRole.DisplayRole:
            return test_type

    def rowCount(self, index):
        return len(self._labtests)
