# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows_interfaces/info_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_info_window(object):
    def setupUi(self, info_window):
        info_window.setObjectName("info_window")
        info_window.resize(400, 300)
        self.information_plaintext = QtWidgets.QPlainTextEdit(info_window)
        self.information_plaintext.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.information_plaintext.setReadOnly(True)
        self.information_plaintext.setObjectName("information_plaintext")

        self.retranslateUi(info_window)
        QtCore.QMetaObject.connectSlotsByName(info_window)

    def retranslateUi(self, info_window):
        _translate = QtCore.QCoreApplication.translate
        info_window.setWindowTitle(_translate("info_window", "Информация о программе"))
