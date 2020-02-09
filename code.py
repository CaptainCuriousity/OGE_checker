from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from windows_interfaces.main_window import Ui_MainWindow
from windows_interfaces.table_window import Ui_TableForm
import sys


class ExamCheckerMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ok_button.clicked.connect(self.show_table)
        self.info_button.clicked.connect(self.show_info)
        self.setFixedSize(self.size())

    def show_table(self):
        school_number = self.school_spinbox.value()
        initials = self.initiels_lineedit.text()
        date = self.date_lineedit.text()

        if len(initials.split(" ")) != 3:
            QMessageBox.critical(
                self, "Ошибка!", "Было неправильно введено ФИО учителя!", QMessageBox.Ok
            )
            return

        if len(date.split(".")) != 3:
            QMessageBox.critical(
                self, "Ошибка!", "Была неправильно введена дата!", QMessageBox.Ok
            )
            return
        else:
            day, month, year = map(int, date.split("."))
            if day < 1 or day > 31 or month < 1 or month > 12 or year < 0:
                QMessageBox.critical(
                    self, "Ошибка!", "Была неправильно введена дата!", QMessageBox.Ok
                )
                return

        self.table_window = ExamCheckerWidget(school_number, initials, date)
        self.table_window.show()

    def show_info(self):
        # TODO: показ информации о работе с программой
        pass


class ExamCheckerWidget(QWidget, Ui_TableForm):
    def __init__(self, school_number, initials, date):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.school_number = school_number
        self.initials = initials
        self.date = date

        window_title = str(school_number) + "--" + initials + "--" + date
        self.setWindowTitle(window_title)

        fields = [
            "ФИО ученика", "Номер варианта", "Класс",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
            "13.1", "13.2", "14.1", "14.2", "14.3", "15.1", "15.2"
        ]
        self.balls_tablewidget.setColumnCount(len(fields))
        self.balls_tablewidget.setHorizontalHeaderLabels(fields)
        self.balls_tablewidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exam_checker = ExamCheckerMainForm()
    exam_checker.show()
    sys.exit(app.exec())
