import sys

from PySide6.QtWidgets import QApplication
from views import MainWindow


def main(args):
    app = QApplication(args)
    app.setStyle("Fusion")

    screen_size = app.primaryScreen().size()

    window = MainWindow()
    window.resize(screen_size)
    window.show()

    app.exec()


if __name__ == "__main__":
    main(sys.argv)
