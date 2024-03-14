from core.template.template import *
from core.strategies.strategies import *
from core.mutations.mutation import mutation

from gui.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())