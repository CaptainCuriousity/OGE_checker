from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from windows_interfaces.main_window import Ui_MainWindow
from windows_interfaces.table_window import Ui_TableForm
from windows_interfaces.info_window import Ui_info_window
import sys
import os
import csv
import xlsxwriter
import sqlite3


class ExamCheckerMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ok_button.clicked.connect(self.show_table)
        self.info_button.clicked.connect(self.show_info)
        self.setFixedSize(self.size())

    def show_table(self):
        school_number = self.school_spinbox.value()
        teacher_initials = self.initiels_lineedit.text()
        date = self.date_lineedit.text()

        if len(teacher_initials.split(" ")) != 3:
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

        self.table_window = ExamCheckerWidget(school_number, teacher_initials, date)
        self.table_window.show()

    def show_info(self):
        self.info_widget = InfoWidget()
        self.info_widget.show()


class InfoWidget(QWidget, Ui_info_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        info = f"""Краткое пособие по работе с программой.
На главной форме вводится ФИО учителя, класс и дата.
На следующий форме есть следующие поля:
ФИО ученика, класс, вариант (все варианты хранятся в папке variants,
в ней должно быть 12 строк для ответов по заданиям с 1-ого по 12-ое)
1-12: задания с кратким ответом. В них вносится ответ ученика. В случае, если он
правильный, ученик получает 1 балл.
13.1, 13.2, 14.1, 14.2, 14.3, 15.1, 15.2: задания с развёрнутым ответом.
Их учитель проверяет самостоятельно и выставляет для 13 и 15 оценки:
1. "не приступал"
2. "0б"
3. "1б"
4. "2б"
И для 14:
1. "не приступал"
2. "0б"
3. "1б"
Кавычки в таблицу ставить не нужно.
Какой максимальный балл за задание учитель выставит,
такой балл ученик и получит.

На форме с таблицей так же есть кнопки, которые делают то, что на них написано.
В случае, если пользователь захочет сделать экспорт в xlsx, то
так же в самом низу таблицы будет написано количество двоек, троек, четвёрок 
и пятёрок по всей таблице, а так же количество баллов и количество учеников,
на них написавших. (количество учеников, написавших на 0 баллов, на 1, на 2 и т.д.)

Внешний вид варианта в папке variants(demo.txt):

ТЮЛЕНЬ|ОБЛАКО|18|8|10|5|7413265|570|10|35|ОВСЯНИКОВ|16

В папке program хранится exe-файл."""

        self.information_plaintext.setPlainText(info)


class ExamCheckerWidget(QWidget, Ui_TableForm):
    def __init__(self, school_number, teacher_initials, date):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.school_number = school_number
        self.teacher_initials = teacher_initials
        self.date = date

        window_title = str(school_number) + "--" + teacher_initials + "--" + date
        self.setWindowTitle(window_title)

        fields = [
            "ФИО ученика", "Номер варианта", "Класс",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
            "13.1", "13.2", "14.1", "14.2", "14.3", "15.1", "15.2", "Результат",
            "Итоговый балл"
        ]
        self.balls_tablewidget.setColumnCount(len(fields))
        self.balls_tablewidget.setHorizontalHeaderLabels(fields)
        self.balls_tablewidget.resizeColumnsToContents()

        self.add_student_button.clicked.connect(self.add_student)
        self.remove_student_button.clicked.connect(self.remove_student)

        self.save_button.clicked.connect(self.save_table)
        self.csv_button.clicked.connect(self.export_into_csv)
        self.xlsx_button.clicked.connect(self.export_into_xlsx)
        self.delete_table_button.clicked.connect(self.delete_table)

        self.update_balls_button.clicked.connect(self.count_balls)

        self.load_table()

    def get_variant_data(self, student_index):
        variant = self.balls_tablewidget.item(student_index, 1).text()
        variant_path = "variants/" + variant + ".txt"
        if not os.path.exists(variant_path):
            QMessageBox.critical(
                self, "Ошибка", f'Варианта "{variant}" не существует (строка {student_index + 1})',
                QMessageBox.Ok
            )
            return
        try:
            with open(variant_path, mode="r", encoding="utf-8") as variant_file:
                variant_text = "".join(
                    filter(lambda x: x.isalnum() or x == "|", variant_file.read())
                )
                variant_data = variant_text.split("|")
                variant_data = list(map(lambda x: x.lower(), variant_data))
                if len(variant_data) != 12:
                    QMessageBox.critical(
                        self, "Ошибка", "Неправильные данные в файле", QMessageBox.Ok
                    )
                    return
        except OSError as error:
            QMessageBox.critical(self, "Ошибка", error.strerror, QMessageBox.Ok)
            return
        return variant_data

    def load_table(self):
        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".db"
        if not os.path.exists("balls_databases/" + filename):
            return
        connection = sqlite3.connect("balls_databases/" + filename)
        cursor = connection.cursor()
        data = cursor.execute("SELECT * FROM student_information").fetchall()
        for row in data:
            index, row_data = row[0], row[1:]
            self.balls_tablewidget.setRowCount(index + 1)
            for j, item in enumerate(row_data):
                self.balls_tablewidget.setItem(index, j, QTableWidgetItem(str(item)))
        self.balls_tablewidget.resizeColumnsToContents()

    def count_balls(self):
        if not os.path.exists("variants"):
            os.mkdir("variants")
        for i in range(self.balls_tablewidget.rowCount()):
            variant_data = self.get_variant_data(i)
            all_tasks_data = []
            for j in range(3, self.balls_tablewidget.columnCount() - 2):
                all_tasks_data.append(self.balls_tablewidget.item(i, j).text().lower())

            balls = 0
            for j in range(12):
                if all_tasks_data[j] == variant_data[j]:
                    balls += 1

            part_2_data = []
            for j in range(12, 19):
                if all_tasks_data[j] == "0б" or all_tasks_data[j] == "0":
                    part_2_data.append(0)
                elif all_tasks_data[j] == "1б" or all_tasks_data[j] == "1":
                    part_2_data.append(1)
                elif (all_tasks_data[j] == "2б" or all_tasks_data[j] == "2") and not 14 <= j <= 16:
                    part_2_data.append(2)
                else:
                    part_2_data.append(0)
            task13_ball = [part_2_data[0], part_2_data[1]]
            task14_ball = [part_2_data[2], part_2_data[3], part_2_data[4]]
            task15_ball = [part_2_data[5], part_2_data[6]]
            balls += max(task13_ball) + sum(task14_ball) + max(task15_ball)

            mark = None
            if 0 <= balls <= 3:
                mark = "2"
            elif 4 <= balls <= 9:
                mark = "3"
            elif 10 <= balls <= 15:
                mark = "4"
            elif 16 <= balls <= 19:
                mark = "5"
            self.balls_tablewidget.setItem(
                i, self.balls_tablewidget.columnCount() - 2, QTableWidgetItem(str(balls))
            )

            self.balls_tablewidget.setItem(
                i, self.balls_tablewidget.columnCount() - 1, QTableWidgetItem(mark)
            )

        self.balls_tablewidget.resizeColumnsToContents()

    def add_student(self):
        new_size = self.balls_tablewidget.rowCount() + 1
        self.balls_tablewidget.setRowCount(new_size)

        self.balls_tablewidget.setItem(new_size - 1, 0, QTableWidgetItem("Пупкин Василий Иванович"))
        self.balls_tablewidget.setItem(new_size - 1, 1, QTableWidgetItem("demo"))
        self.balls_tablewidget.setItem(new_size - 1, 2, QTableWidgetItem("9А"))

        for i in range(3, self.balls_tablewidget.columnCount() - 2):
            self.balls_tablewidget.setItem(
                new_size - 1, i, QTableWidgetItem("не приступал")
            )

        self.balls_tablewidget.setItem(
            new_size - 1, self.balls_tablewidget.columnCount() - 2, QTableWidgetItem("0")
        )

        self.balls_tablewidget.setItem(
            new_size - 1, self.balls_tablewidget.columnCount() - 1, QTableWidgetItem("2")
        )
        self.balls_tablewidget.resizeColumnsToContents()

    def remove_student(self):
        if not self.balls_tablewidget.selectedIndexes():
            return

        student_row = self.balls_tablewidget.selectedIndexes()[0].row()
        self.balls_tablewidget.removeRow(student_row)

    def write_default_table_data(self):
        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".db"
        open("balls_databases/" + filename, mode="tw", encoding="utf-8").close()
        connection = sqlite3.connect("balls_databases/" + filename)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE teacher_information
            (date                   STRING,
            teacher_initials        STRING,
            school_number           STRING
            );"""
        )
        cursor.execute(
            """CREATE TABLE student_information
            (id                     INTEGER PRIMARY KEY AUTOINCREMENT,
            initials                STRING,
            variant                 STRING,
            class                   STRING,
            task1                   STRING,
            task2                   STRING,
            task3                   STRING,
            task4                   STRING,
            task5                   STRING,
            task6                   STRING,
            task7                   STRING,
            task8                   STRING,
            task9                   STRING,
            task10                  STRING,
            task11                  STRING,
            task12                  STRING,
            task13_1                STRING,
            task13_2                STRING,
            task14_1                STRING,
            task14_2                STRING,
            task14_3                STRING,
            task15_1                STRING,
            task15_2                STRING,
            result_balls            STRING,
            mark                    STRING
            );"""
        )
        cursor.execute(
            f"""
            INSERT INTO teacher_information(date, teacher_initials, school_number)
            VALUES ("{self.date}",
            "{self.teacher_initials}", {str(self.school_number)})"""
        )

        connection.commit()
        connection.close()

    def save_table(self):
        self.count_balls()

        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".db"
        if not os.path.exists("balls_databases"):
            os.mkdir("balls_databases")

        if not os.path.exists("balls_databases/" + filename):
            open("balls_databases/" + filename, mode="tw", encoding="utf-8").close()
            self.write_default_table_data()

        connection = sqlite3.connect("balls_databases/" + filename)
        cursor = connection.cursor()
        cursor.execute(
            f"""DELETE FROM student_information"""
        )
        for i in range(self.balls_tablewidget.rowCount()):
            data_to_write = []
            for j in range(self.balls_tablewidget.columnCount()):
                data_to_write.append(self.balls_tablewidget.item(i, j).text())
            data_to_write = repr(data_to_write)[1:-1]
            cursor.execute(f"""INSERT INTO student_information VALUES ({i}, {data_to_write})""")
        connection.commit()
        connection.close()

    def delete_table(self):
        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".db"
        if os.path.exists("balls_databases/" + filename):
            try:
                os.remove("balls_databases/" + filename)
            except OSError as error:
                QMessageBox.critical(self, "Ошибка", error.strerror, QMessageBox.Ok)
                return
        self.balls_tablewidget.clear()
        self.balls_tablewidget.setRowCount(0)

        fields = [
            "ФИО ученика", "Номер варианта", "Класс",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
            "13.1", "13.2", "14.1", "14.2", "14.3", "15.1", "15.2", "Результат",
            "Итоговый балл"
        ]
        self.balls_tablewidget.setColumnCount(len(fields))
        self.balls_tablewidget.setHorizontalHeaderLabels(fields)
        self.balls_tablewidget.resizeColumnsToContents()

    def export_into_csv(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку") + "/"
        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".csv"
        if os.path.exists(path + filename):
            os.remove(path + filename)
        with open(path + filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([self.balls_tablewidget.horizontalHeaderItem(i).text()
                             for i in range(self.balls_tablewidget.columnCount())])
            for i in range(self.balls_tablewidget.rowCount()):
                row = []
                for j in range(self.balls_tablewidget.columnCount()):
                    item = self.balls_tablewidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                    else:
                        row.append("NULL")
                writer.writerow(row)

    def export_into_xlsx(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку") + "/"
        filename = "-".join([str(self.school_number), self.teacher_initials, self.date]) + ".xlsx"
        if os.path.exists(path + filename):
            os.remove(path + filename)

        workbook = xlsxwriter.Workbook(path + filename)
        worksheet = workbook.add_worksheet()

        for j in range(self.balls_tablewidget.columnCount()):
            worksheet.write(0, j, self.balls_tablewidget.horizontalHeaderItem(j).text())

        for i in range(self.balls_tablewidget.rowCount()):
            all_tasks_data = []
            variant_data = self.get_variant_data(i)
            for j in range(self.balls_tablewidget.columnCount()):
                worksheet.write(2 * i + 1, j, self.balls_tablewidget.item(i, j).text())
                if 3 <= j < self.balls_tablewidget.columnCount() - 2:
                    all_tasks_data.append(self.balls_tablewidget.item(i, j).text().lower())

            pass_balls = []
            for j in range(12):
                pass_balls.append(1 if variant_data[j] == all_tasks_data[j] else 0)

            part_2_data = []
            for j in range(12, 19):
                if all_tasks_data[j] == "0б" or all_tasks_data[j] == "0":
                    part_2_data.append(0)
                elif all_tasks_data[j] == "1б" or all_tasks_data[j] == "1":
                    part_2_data.append(1)
                elif (all_tasks_data[j] == "2б" or all_tasks_data[j] == "2") and not 14 <= j <= 16:
                    part_2_data.append(2)
                else:
                    part_2_data.append(0)

            task13_ball = [part_2_data[0], part_2_data[1]]
            task14_ball = [part_2_data[2], part_2_data[3], part_2_data[4]]
            task15_ball = [part_2_data[5], part_2_data[6]]

            task13_ball = [max(task13_ball)] * 2
            task15_ball = [max(task15_ball)] * 2

            pass_balls.extend(task13_ball)
            pass_balls.extend(task14_ball)
            pass_balls.extend(task15_ball)

            for j in range(3, self.balls_tablewidget.columnCount() - 2):
                worksheet.write(2 * i + 2, j, pass_balls[j - 3])

        balls_count_list = [0] * 20
        marks_count_dict = {"2": 0, "3": 0, "4": 0, "5": 0}
        for i in range(self.balls_tablewidget.rowCount()):
            ball = self.balls_tablewidget.item(i, self.balls_tablewidget.columnCount() - 2).text()
            mark = self.balls_tablewidget.item(i, self.balls_tablewidget.columnCount() - 1).text()
            marks_count_dict[mark] += 1
            balls_count_list[int(ball)] += 1

        worksheet.write_row(
            self.balls_tablewidget.rowCount() * 2 + 5, 0, ["Оценка", "Частота встречаемости оценки"]
        )
        for i, (k, v) in enumerate(marks_count_dict.items()):
            worksheet.write_row(self.balls_tablewidget.rowCount() * 2 + i + 6, 0, [k, v])

        worksheet.write_row(
            self.balls_tablewidget.rowCount() * 2 + 5, 4, ["Балл", "Частота встречаемости балла"]
        )
        for i, count in enumerate(balls_count_list):
            worksheet.write_row(
                self.balls_tablewidget.rowCount() * 2 + i + 6, 4, [str(i), count]
            )
        workbook.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exam_checker = ExamCheckerMainForm()
    exam_checker.show()
    sys.exit(app.exec())
