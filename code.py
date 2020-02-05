from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class OGE_checker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Проверка ОГЭ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = OGE_checker()
    main_app.show()
    sys.exit(app.exec())
