import shutil
import appUI002
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import fitz
import os
import pdf_pretreat
import pdf_identifather
import pytesseract
import img_pretreat
import sys
import cv2
import identifather


class MyWindow(QMainWindow, appUI002.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.progressBar.setVisible(False)

        self.name_char_but.clicked.connect(lambda x: self.progressBar.setVisible(True))

        # 建立表格
        self.set_form()

        self.pdf_set_form()

        # 处理图片界面槽
        self.img_but.clicked.connect(self.LoadRawImage)

        self.form_but.clicked.connect(self.form_show)

        self.name_char_but.clicked.connect(self.load_char)

        # pdf文件处理界面槽
        self.pdf_but.clicked.connect(self.load_pdf)

        self.PdfAct_but.clicked.connect(self.pdf_form_show)



    """
    1. 图片处理界面
    """

    def set_form(self): # 表格初始化

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(['人物主体', '识别内容', '父亲主体', '父亲姓名'])

        self.table.setIconSize(QSize(300, 200))

    def LoadRawImage(self): # 选择图片文件
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", "../", "图像文件(*.jpg *.png)")

        self.img_linetext.setText(fname)
        pic = QPixmap(fname)
        self.img_lab.setPixmap(pic.scaled(self.img_lab.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def form_show(self):    # 人物关系展示

        fname = self.img_linetext.text()

        if len(fname) == 0:
            QMessageBox.critical(self, '错误', '未选择图片')
            return 0

        if os.path.exists(r'out') == False:
            os.mkdir(r'out')
        if os.path.exists(r'out') == True:
            file_list = os.listdir(r'out')
            for i in file_list:
                waste_file = 'out' + '/' + i
                os.remove(waste_file)

        coordinates = img_pretreat.clude_name(fname)
        img = cv2.imread(r'out/result.jpg')

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(2, 150)

        relation_dict = identifather.relation_integration_dict(coordinates)
        self.table.setRowCount(len(coordinates))

        for j in range(len(coordinates)):
            self.table.setRowHeight(j, 80)

        i = 0
        for kid_cod, father_cod in relation_dict.items():

            if type(father_cod) != str:  # 除了根节点外

                x1, y1, x2, y2 = kid_cod
                u1, v1, u2, v2 = father_cod

                kid_area = img[y1:y2, x1:x2]
                father_area = img[v1:v2, u1:u2]

                # 处理numpy类型图片
                kid_area = cv2.cvtColor(kid_area, cv2.COLOR_BGR2RGB)
                kid_area = QImage(kid_area[:], kid_area.shape[1], kid_area.shape[0], kid_area.shape[1] * 3,
                                  QImage.Format_RGB888)

                father_area = cv2.cvtColor(father_area, cv2.COLOR_BGR2RGB)
                father_area = QImage(father_area[:], father_area.shape[1], father_area.shape[0],
                                     father_area.shape[1] * 3, QImage.Format_RGB888)

                kid_icon = QIcon(QPixmap(kid_area))
                father_ico = QIcon(QPixmap(father_area))

                kid_item = QTableWidgetItem()
                father_item = QTableWidgetItem()

                kid_item.setIcon(kid_icon)
                father_item.setIcon(father_ico)

                self.table.setItem(i, 0, kid_item)
                self.table.setItem(i, 2, father_item)

                i = i + 1
            else:
                x1, y1, x2, y2 = kid_cod
                kid_area = img[y1:y2, x1:x2]
                kid_area = cv2.cvtColor(kid_area, cv2.COLOR_BGR2RGB)
                kid_area = QImage(kid_area[:], kid_area.shape[1], kid_area.shape[0], kid_area.shape[1] * 3,
                                  QImage.Format_RGB888)
                kid_icon = QIcon(QPixmap(kid_area))
                kid_item = QTableWidgetItem()
                kid_item.setIcon(kid_icon)

                self.table.setItem(i, 0, kid_item)

                i = i+1

    def load_char(self):    # OCR识别

        if os.path.exists('out') == False or os.path.exists('out/result.jpg') == False:
            QMessageBox.critical(self, '错误', '未进行图片预处理')
            return 0

        img = cv2.imread(r'out/result.jpg')

        coordinates = img_pretreat.clude_name(self.img_linetext.text())

        relation = identifather.relation_integration(coordinates)
        i = 0
        for item in relation:
            kid_cod, father_cod = item
            if type(father_cod) != str:
                x1, y1, x2, y2 = kid_cod
                u1, v1, u2, v2 = father_cod
                kid_area = img[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
                father_area = img[v1 - 10:v2 + 10, u1 - 10:u2 + 10]
                kid_char = pytesseract.image_to_string(kid_area, lang='chi_sim',
                                                       config='--psm 7, --oem 1, -c max_characters_to_try=2')
                father_char = pytesseract.image_to_string(father_area, lang='chi_sim',
                                                          config='--psm 7, --oem 1, -c max_characters_to_try=2')
                item_kid = QTableWidgetItem(kid_char)
                item_father = QTableWidgetItem(father_char)
                self.table.setItem(i, 1, item_kid)
                self.table.setItem(i, 3, item_father)
                i = i + 1
            else:
                x1, y1, x2, y2 = kid_cod
                kid_area = img[y1 - 10:y2 + 10, x1 - 10:x2 + 10]
                kid_char = pytesseract.image_to_string(kid_area, lang='chi_sim',
                                                       config='--psm 7, --oem 1, -c max_characters_to_try=2')
                item_kid = QTableWidgetItem(kid_char)
                self.table.setItem(i, 1, item_kid)
                item_father = QTableWidgetItem('根节点')
                self.table.setItem(i, 3, item_father)

                i = i + 1

    """
    2. pdf文件处理界面函数
    """

    def pdf_set_form(self): # 表格初始化
        self.pdf_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pdf_table.setColumnCount(4)
        self.pdf_table.setHorizontalHeaderLabels(['人物主体', '识别内容', '父亲主体', '父亲姓名'])
        self.table.setIconSize(QSize(300,200))

    def load_pdf(self): # 选中pdf文件
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", "../", "pdf文件(*.pdf)")
        self.pdf_linetext.setText(fname)

    def pdf_form_show(self):    # pdf文件人物关系展示

        fname = self.pdf_linetext.text()

        if len(fname) == 0:
            QMessageBox.critical(self, '错误', '未选择文件')
            return 0

        file = fitz.open(fname)
        start_page = self.start_spbox.value()
        end_page = self.end_spbox.value()

        # 起始页大于结束页的错误信息
        if start_page - end_page > 1:
            QMessageBox.warning(self, "警告", "起始页大于结束页！", QMessageBox.Yes)
            return 0

        if os.path.exists(r'out') == False:
            os.mkdir(r'out')
        if os.path.exists(r'out') == True:
            file_list = os.listdir(r'out')
            for i in file_list:
                waste_file = 'out' + '/' + i
                os.remove(waste_file)

        if end_page == 0:  # 默认
            for pg in range(3):  # doc.page_count
                page = file[pg]
                rotate = int(0)
                # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
                zoom_x = 2.0
                zoom_y = 2.0
                trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
                pm = page.get_pixmap(matrix=trans, alpha=True)
                pm.save('out/page{}.jpg'.format(pg))
        else:
            for pg in range(start_page - 1, end_page):
                page = file[pg]
                rotate = int(0)
                # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
                zoom_x = 2.0
                zoom_y = 2.0
                trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
                pm = page.get_pixmap(matrix=trans, alpha=True)
                pm.save('out/page{}.jpg'.format(pg))

        start_page = self.start_spbox.value()
        end_page = self.end_spbox.value()

        if end_page == 0:
            faultEvent = len(os.listdir(r'out')) != 3
        else:
            faultEvent = len(os.listdir(r'out')) != end_page - start_page + 1
        if faultEvent:
            QMessageBox.warning(self, '警告', '程序已经运行')
            return 0

        if os.path.exists('out') == False or len(os.listdir(r'out')) == 0:
            QMessageBox.critical(self, '错误', '文件未进行预处理!')
            return 0

        self.pdf_table.setColumnWidth(0, 170)
        self.pdf_table.setColumnWidth(2, 170)
        self.pdf_table.setRowCount(1)

        img_dir = []
        for (dirname, subdir, files) in os.walk(r'out'):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg':
                    img_dir.append(os.path.join(dirname, file))

        row = 0  # 行数

        for img in img_dir:
            coordinates = pdf_pretreat.clude_name(img)
            relation_dict = pdf_identifather.PdfRelation_integration_dict_backup(coordinates)
            self.pdf_table.setRowCount(self.pdf_table.rowCount() + len(coordinates))
            pic = cv2.imread(r'out/result.jpg')

            for kid_cod, father_cod in relation_dict.items():
                if type(father_cod) != str:  # 除了根节点外

                    x1, y1, x2, y2 = kid_cod
                    u1, v1, u2, v2 = father_cod

                    kid_area = pic[y1:y2, x1:x2]
                    father_area = pic[v1:v2, u1:u2]

                    # 处理numpy类型图片
                    kid_area = cv2.cvtColor(kid_area, cv2.COLOR_BGR2RGB)
                    kid_area = QImage(kid_area[:], kid_area.shape[1], kid_area.shape[0],
                                      kid_area.shape[1] * 3, QImage.Format_RGB888)

                    father_area = cv2.cvtColor(father_area, cv2.COLOR_BGR2RGB)
                    father_area = QImage(father_area[:], father_area.shape[1], father_area.shape[0],
                                         father_area.shape[1] * 3, QImage.Format_RGB888)

                    kid_icon = QIcon(QPixmap(kid_area))
                    father_icon = QIcon(QPixmap(father_area))

                    kid_item = QTableWidgetItem()
                    father_item = QTableWidgetItem()

                    kid_item.setIcon(kid_icon)
                    father_item.setIcon(father_icon)

                    self.pdf_table.setItem(row, 0, kid_item)
                    self.pdf_table.setItem(row, 2, father_item)

                    row = row + 1
                else:  # 根节点
                    x1, y1, x2, y2 = kid_cod
                    kid_area = pic[y1:y2, x1:x2]
                    kid_area = cv2.cvtColor(kid_area, cv2.COLOR_BGR2RGB)
                    kid_area = QImage(kid_area[:], kid_area.shape[1], kid_area.shape[0], kid_area.shape[1] * 3,
                                      QImage.Format_RGB888)

                    kid_area.scaled(170, 80)

                    kid_icon = QIcon(QPixmap(kid_area))
                    kid_item = QTableWidgetItem()
                    kid_item.setIcon(kid_icon)

                    self.pdf_table.setItem(row, 0, kid_item)

                    row = row + 1

        for j in range(self.pdf_table.rowCount()):
            self.pdf_table.setRowHeight(j, 80)

        self.pdf_table.setIconSize(QSize(150, 100))


    """
    3. 清除缓存
    """

    def delete_allwaste(self):
        if os.path.exists('out'):
            shutil.rmtree('out')
        else:
            pass

    def closeEvent(self, event):        # 关闭窗口触发以下事件
        a = QMessageBox.question(self, '退出', '你确定要退出吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            event.accept()
            if os.path.exists('out'):
                shutil.rmtree('out')    # 接受关闭事件

        else:
            event.ignore()        # 忽略关闭事件


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
