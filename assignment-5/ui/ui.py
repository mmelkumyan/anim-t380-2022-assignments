# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sphereGenerator.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(333, 76)
        self.radius_slider = QtWidgets.QSlider(Dialog)
        self.radius_slider.setGeometry(QtCore.QRect(60, 10, 160, 22))
        self.radius_slider.setOrientation(QtCore.Qt.Horizontal)
        self.radius_slider.setObjectName("radius_slider")
        self.radius_label = QtWidgets.QLabel(Dialog)
        self.radius_label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.radius_label.setObjectName("radius_label")
        self.generate_button = QtWidgets.QPushButton(Dialog)
        self.generate_button.setGeometry(QtCore.QRect(230, 40, 75, 23))
        self.generate_button.setObjectName("generate_button")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(230, 10, 71, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radius_label.setText(_translate("Dialog", "Radius"))
        self.generate_button.setText(_translate("Dialog", "Generate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())