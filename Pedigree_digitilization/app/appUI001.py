# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appUI001.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 834)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 841, 731))
        self.tabWidget.setObjectName("tabWidget")
        self.img_tab = QtWidgets.QWidget()
        self.img_tab.setObjectName("img_tab")
        self.table = QtWidgets.QTableWidget(self.img_tab)
        self.table.setGeometry(QtCore.QRect(10, 10, 611, 411))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.dir_hint = QtWidgets.QLabel(self.img_tab)
        self.dir_hint.setGeometry(QtCore.QRect(70, 510, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dir_hint.setFont(font)
        self.dir_hint.setObjectName("dir_hint")
        self.format_lab = QtWidgets.QLabel(self.img_tab)
        self.format_lab.setGeometry(QtCore.QRect(240, 450, 171, 16))
        self.format_lab.setObjectName("format_lab")
        self.if_show_chekbox = QtWidgets.QCheckBox(self.img_tab)
        self.if_show_chekbox.setEnabled(True)
        self.if_show_chekbox.setGeometry(QtCore.QRect(260, 620, 120, 22))
        self.if_show_chekbox.setChecked(True)
        self.if_show_chekbox.setObjectName("if_show_chekbox")
        self.img_linetext = QtWidgets.QLineEdit(self.img_tab)
        self.img_linetext.setEnabled(False)
        self.img_linetext.setGeometry(QtCore.QRect(70, 540, 261, 21))
        self.img_linetext.setReadOnly(True)
        self.img_linetext.setObjectName("img_linetext")
        self.img_but = QtWidgets.QPushButton(self.img_tab)
        self.img_but.setGeometry(QtCore.QRect(60, 440, 161, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_but.sizePolicy().hasHeightForWidth())
        self.img_but.setSizePolicy(sizePolicy)
        self.img_but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.img_but.setObjectName("img_but")
        self.img_lab = QtWidgets.QLabel(self.img_tab)
        self.img_lab.setGeometry(QtCore.QRect(430, 430, 211, 261))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_lab.sizePolicy().hasHeightForWidth())
        self.img_lab.setSizePolicy(sizePolicy)
        self.img_lab.setText("")
        self.img_lab.setObjectName("img_lab")
        self.layoutWidget = QtWidgets.QWidget(self.img_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(650, 10, 161, 401))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.act_but = QtWidgets.QPushButton(self.layoutWidget)
        self.act_but.setObjectName("act_but")
        self.verticalLayout.addWidget(self.act_but)
        self.hint_lab = QtWidgets.QLabel(self.layoutWidget)
        self.hint_lab.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hint_lab.sizePolicy().hasHeightForWidth())
        self.hint_lab.setSizePolicy(sizePolicy)
        self.hint_lab.setText("")
        self.hint_lab.setObjectName("hint_lab")
        self.verticalLayout.addWidget(self.hint_lab)
        self.form_but = QtWidgets.QPushButton(self.layoutWidget)
        self.form_but.setEnabled(True)
        self.form_but.setObjectName("form_but")
        self.verticalLayout.addWidget(self.form_but)
        self.name_char_but = QtWidgets.QPushButton(self.layoutWidget)
        self.name_char_but.setObjectName("name_char_but")
        self.verticalLayout.addWidget(self.name_char_but)
        self.tabWidget.addTab(self.img_tab, "")
        self.pdf_tab = QtWidgets.QWidget()
        self.pdf_tab.setObjectName("pdf_tab")
        self.PdfDir_hint = QtWidgets.QLabel(self.pdf_tab)
        self.PdfDir_hint.setGeometry(QtCore.QRect(70, 510, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.PdfDir_hint.setFont(font)
        self.PdfDir_hint.setObjectName("PdfDir_hint")
        self.PdfFomat_lab = QtWidgets.QLabel(self.pdf_tab)
        self.PdfFomat_lab.setGeometry(QtCore.QRect(240, 450, 171, 16))
        self.PdfFomat_lab.setObjectName("PdfFomat_lab")
        self.pdf_table = QtWidgets.QTableWidget(self.pdf_tab)
        self.pdf_table.setGeometry(QtCore.QRect(10, 10, 611, 411))
        self.pdf_table.setObjectName("pdf_table")
        self.pdf_table.setColumnCount(0)
        self.pdf_table.setRowCount(0)
        self.pdf_linetext = QtWidgets.QLineEdit(self.pdf_tab)
        self.pdf_linetext.setEnabled(False)
        self.pdf_linetext.setGeometry(QtCore.QRect(70, 540, 261, 21))
        self.pdf_linetext.setReadOnly(True)
        self.pdf_linetext.setObjectName("pdf_linetext")
        self.layoutWidget_4 = QtWidgets.QWidget(self.pdf_tab)
        self.layoutWidget_4.setGeometry(QtCore.QRect(640, 10, 171, 401))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.PdfAct_but = QtWidgets.QPushButton(self.layoutWidget_4)
        self.PdfAct_but.setObjectName("PdfAct_but")
        self.verticalLayout_2.addWidget(self.PdfAct_but)
        self.PdfHint_lab = QtWidgets.QLabel(self.layoutWidget_4)
        self.PdfHint_lab.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PdfHint_lab.sizePolicy().hasHeightForWidth())
        self.PdfHint_lab.setSizePolicy(sizePolicy)
        self.PdfHint_lab.setText("")
        self.PdfHint_lab.setObjectName("PdfHint_lab")
        self.verticalLayout_2.addWidget(self.PdfHint_lab)
        self.PdfForm_but = QtWidgets.QPushButton(self.layoutWidget_4)
        self.PdfForm_but.setEnabled(True)
        self.PdfForm_but.setObjectName("PdfForm_but")
        self.verticalLayout_2.addWidget(self.PdfForm_but)
        self.Pdfname_char_but = QtWidgets.QPushButton(self.layoutWidget_4)
        self.Pdfname_char_but.setObjectName("Pdfname_char_but")
        self.verticalLayout_2.addWidget(self.Pdfname_char_but)
        self.pdf_but = QtWidgets.QPushButton(self.pdf_tab)
        self.pdf_but.setGeometry(QtCore.QRect(60, 440, 161, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pdf_but.sizePolicy().hasHeightForWidth())
        self.pdf_but.setSizePolicy(sizePolicy)
        self.pdf_but.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pdf_but.setObjectName("pdf_but")
        self.start_spbox = QtWidgets.QSpinBox(self.pdf_tab)
        self.start_spbox.setGeometry(QtCore.QRect(90, 580, 71, 31))
        self.start_spbox.setProperty("value", 1)
        self.start_spbox.setObjectName("start_spbox")
        self.end_spbox = QtWidgets.QSpinBox(self.pdf_tab)
        self.end_spbox.setGeometry(QtCore.QRect(240, 580, 71, 31))
        self.end_spbox.setObjectName("end_spbox")
        self.label = QtWidgets.QLabel(self.pdf_tab)
        self.label.setGeometry(QtCore.QRect(50, 570, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.pdf_tab)
        self.label_2.setGeometry(QtCore.QRect(170, 570, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.pdf_tab)
        self.label_3.setGeometry(QtCore.QRect(320, 570, 71, 51))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.pdf_tab)
        self.label_4.setGeometry(QtCore.QRect(220, 620, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.pdf_tab, "")
        self.close_but = QtWidgets.QPushButton(self.centralwidget)
        self.close_but.setGeometry(QtCore.QRect(700, 760, 141, 31))
        self.close_but.setObjectName("close_but")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.close_but.clicked.connect(MainWindow.close)
        self.if_show_chekbox.toggled['bool'].connect(self.img_lab.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "族谱识别系统0.0.1"))
        self.dir_hint.setText(_translate("MainWindow", "图片路径："))
        self.format_lab.setText(_translate("MainWindow", "(*jpg, *jpeg, *png格式图片)"))
        self.if_show_chekbox.setText(_translate("MainWindow", "显示/不显示图片"))
        self.img_but.setText(_translate("MainWindow", "0.选择目标图片"))
        self.act_but.setText(_translate("MainWindow", "1. 图像文件预处理"))
        self.form_but.setText(_translate("MainWindow", "2.人物关系显示"))
        self.name_char_but.setText(_translate("MainWindow", "3.识别姓名"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.img_tab), _translate("MainWindow", "图像文件"))
        self.PdfDir_hint.setText(_translate("MainWindow", "文件路径："))
        self.PdfFomat_lab.setText(_translate("MainWindow", "(*pdf文件)"))
        self.PdfAct_but.setText(_translate("MainWindow", "1.文件预处理"))
        self.PdfForm_but.setText(_translate("MainWindow", "2.人物关系显示"))
        self.Pdfname_char_but.setText(_translate("MainWindow", "3.识别姓名（待上线）"))
        self.pdf_but.setText(_translate("MainWindow", "0.选择pdf文件"))
        self.label.setText(_translate("MainWindow", "第"))
        self.label_2.setText(_translate("MainWindow", "页 ～ 第"))
        self.label_3.setText(_translate("MainWindow", "页"))
        self.label_4.setText(_translate("MainWindow", "*（默认为文件前3页）"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pdf_tab), _translate("MainWindow", "pdf文件"))
        self.close_but.setText(_translate("MainWindow", "关闭"))

