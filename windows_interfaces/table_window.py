# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows_interfaces/table_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TableForm(object):
    def setupUi(self, TableForm):
        TableForm.setObjectName("TableForm")
        TableForm.resize(800, 630)
        self.balls_tablewidget = QtWidgets.QTableWidget(TableForm)
        self.balls_tablewidget.setGeometry(QtCore.QRect(10, 10, 781, 491))
        self.balls_tablewidget.setObjectName("balls_tablewidget")
        self.balls_tablewidget.setColumnCount(0)
        self.balls_tablewidget.setRowCount(0)
        self.save_button = QtWidgets.QPushButton(TableForm)
        self.save_button.setGeometry(QtCore.QRect(620, 520, 141, 31))
        self.save_button.setObjectName("save_button")
        self.xlsx_button = QtWidgets.QPushButton(TableForm)
        self.xlsx_button.setGeometry(QtCore.QRect(480, 520, 121, 31))
        self.xlsx_button.setObjectName("xlsx_button")
        self.csv_button = QtWidgets.QPushButton(TableForm)
        self.csv_button.setGeometry(QtCore.QRect(480, 570, 121, 31))
        self.csv_button.setObjectName("csv_button")
        self.add_student_button = QtWidgets.QPushButton(TableForm)
        self.add_student_button.setGeometry(QtCore.QRect(30, 520, 221, 28))
        self.add_student_button.setObjectName("add_student_button")
        self.remove_student_button = QtWidgets.QPushButton(TableForm)
        self.remove_student_button.setGeometry(QtCore.QRect(30, 570, 221, 28))
        self.remove_student_button.setObjectName("remove_student_button")
        self.delete_table_button = QtWidgets.QPushButton(TableForm)
        self.delete_table_button.setGeometry(QtCore.QRect(620, 570, 141, 28))
        self.delete_table_button.setObjectName("delete_table_button")
        self.update_balls_button = QtWidgets.QPushButton(TableForm)
        self.update_balls_button.setGeometry(QtCore.QRect(260, 520, 211, 31))
        self.update_balls_button.setObjectName("update_balls_button")

        self.retranslateUi(TableForm)
        QtCore.QMetaObject.connectSlotsByName(TableForm)

    def retranslateUi(self, TableForm):
        _translate = QtCore.QCoreApplication.translate
        TableForm.setWindowTitle(_translate("TableForm", "Form"))
        self.save_button.setText(_translate("TableForm", "Сохранить"))
        self.xlsx_button.setText(_translate("TableForm", "Экспорт в xlsx"))
        self.csv_button.setText(_translate("TableForm", "Экспорт в csv"))
        self.add_student_button.setText(_translate("TableForm", "Добавить нового ученика"))
        self.remove_student_button.setText(_translate("TableForm", "Удалить ученика"))
        self.delete_table_button.setText(_translate("TableForm", "Удалить таблицу"))
        self.update_balls_button.setText(_translate("TableForm", "Обновить баллы"))
