# -*- coding: utf-8 -*-
import datetime
import logging
# Form implementation generated from reading ui file 'code_change.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import sys
import time
from datetime import date

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from day01.poxy import MyGit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 868)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(200, 60, 401, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(200, 220, 401, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # self.comboBox.currentIndexChanged.connect(self.get_api)  # 当选择内容改变时触发事件
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 60, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 220, 61, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 140, 91, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 180, 91, 21))
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(200, 350, 701, 461))
        self.textBrowser.setObjectName("textBrowser")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 350, 61, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 260, 51, 16))
        self.label_6.setObjectName("label_6")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(200, 260, 401, 71))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 100, 51, 21))
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(200, 100, 401, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(200, 140, 401, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(200, 180, 401, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 180, 75, 23))
        self.pushButton.setObjectName("pushButton")

        # 绑定按钮事件
        self.pushButton.clicked.connect(self.run)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "代码差异化分析"))
        self.comboBox.setItemText(0, _translate("MainWindow", "全部"))
        self.label.setText(_translate("MainWindow", "项目路径："))
        self.label_2.setText(_translate("MainWindow", "变更文件："))
        self.label_3.setText(_translate("MainWindow", "Source branch："))
        self.label_4.setText(_translate("MainWindow", "Target branch："))
        self.label_5.setText(_translate("MainWindow", "日志："))
        self.label_6.setText(_translate("MainWindow", "变更接口："))
        self.label_7.setText(_translate("MainWindow", "仓库地址："))
        self.pushButton.setText(_translate("MainWindow", "开始比对"))

    def get_api(self):
        print(self.comboBox.itemText())


    def set_textbrowser(self,content,color = None):
        _translate = QtCore.QCoreApplication.translate
        return self.textBrowser.append(_translate("MainWindow", '<span><font color=\"%s\">%s</font></span>' %(color,'> '+ time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())+"-INFO    "+ content)))



    def run(self):
        _translate = QtCore.QCoreApplication.translate
        local_path = self.lineEdit.text()
        repo_url = self.lineEdit_5.text()
        source_branch = self.lineEdit_6.text()
        target_branch = self.lineEdit_7.text()
        self.set_textbrowser("开始执行........")
        self.set_textbrowser("获取变更记录........")

        # 获取所有变更文件
        mgit = MyGit(local_path, repo_url)
        change_record = mgit.get_change_line(source_branch, target_branch)
        self.set_textbrowser(change_record)

        change_files = mgit.diff_files(source_branch, target_branch)

        self.set_textbrowser("开始获取变更文件........")




        if change_files.__len__()<1:
            self.set_textbrowser("没有更新的文件！","red")
        if change_files != '':
            change_files = change_files.split('\n')
            self.comboBox.addItems(change_files)
            for i in range(change_files.__len__()):
                self.set_textbrowser(change_files[i])
            try:
                apis = mgit.get_change_apis(source_branch,target_branch,change_files)
                if len(apis)<1:
                    self.set_textbrowser("接口未发生变更！", "green")
                else:
                    for api in apis:
                        for key,value in api.items():
                            if isinstance(value,str):
                                if value not in self.textBrowser_2.toPlainText():
                                    self.textBrowser_2.append(_translate("MainWindow", value))
                            if isinstance(value,list):
                                for v in value:
                                    if v not in self.textBrowser_2.toPlainText():
                                        self.textBrowser_2.append(_translate("MainWindow", v))
                    self.set_textbrowser("接口识别完成！", "green")
            except Exception as e:
                self.set_textbrowser("服务解析异常！","red")
                self.set_textbrowser(e, "red")














if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

