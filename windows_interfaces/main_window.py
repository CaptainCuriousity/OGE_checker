# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows_interfaces/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setGeometry(QtCore.QRect(250, 250, 101, 31))
        self.ok_button.setObjectName("ok_button")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 551, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(10, 10, 0, 0)
        self.formLayout.setHorizontalSpacing(15)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.school_label = QtWidgets.QLabel(self.layoutWidget)
        self.school_label.setObjectName("school_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.school_label)
        self.school_spinbox = QtWidgets.QSpinBox(self.layoutWidget)
        self.school_spinbox.setMinimum(1)
        self.school_spinbox.setMaximum(1000)
        self.school_spinbox.setProperty("value", 42)
        self.school_spinbox.setObjectName("school_spinbox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.school_spinbox)
        self.initials_label = QtWidgets.QLabel(self.layoutWidget)
        self.initials_label.setObjectName("initials_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.initials_label)
        self.initiels_lineedit = QtWidgets.QLineEdit(self.layoutWidget)
        self.initiels_lineedit.setObjectName("initiels_lineedit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.initiels_lineedit)
        self.date_label = QtWidgets.QLabel(self.layoutWidget)
        self.date_label.setObjectName("date_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.date_label)
        self.date_lineedit = QtWidgets.QLineEdit(self.layoutWidget)
        self.date_lineedit.setObjectName("date_lineedit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_lineedit)
        self.info_button = QtWidgets.QPushButton(self.centralwidget)
        self.info_button.setGeometry(QtCore.QRect(180, 290, 231, 41))
        self.info_button.setObjectName("info_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Проверка ОГЭ"))
        self.ok_button.setText(_translate("MainWindow", "OK"))
        self.school_label.setText(_translate("MainWindow", "Номер школы:"))
        self.initials_label.setText(_translate("MainWindow", "ФИО учителя:"))
        self.initiels_lineedit.setText(_translate("MainWindow", "Зубов Алексей Александрович"))
        self.date_label.setText(_translate("MainWindow", "Дата экзамена(дд/мм/гггг):"))
        self.date_lineedit.setText(_translate("MainWindow", "18.02.2020"))
        self.info_button.setText(_translate("MainWindow", "Информация о программе"))
