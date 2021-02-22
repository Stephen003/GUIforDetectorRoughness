from cv2 import cv2
import numpy as np
import sys
import re
import os

from PySide2.QtWidgets import QFileDialog, QApplication, QDialog, QMainWindow, QPushButton, QPlainTextEdit, QLabel, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QMessageBox
from PySide2.QtGui import QImage, QPixmap
from PySide2 import QtCore

class windowImg(QWidget):
    def __init__(self, parent=None):
        super(windowImg, self).__init__(parent)
        
        self.timerCamera = QtCore.QTimer()  # 定时器
        self.cap = cv2.VideoCapture()  # 摄像头
        self.CAM_NUM = 0
        
        self.initUI()
        self.initSlot()
        
        self.flagCamera = False
        
    def initUI(self):
        # self.setGeometry(60, 60, 1600, 900)
        self.setWindowTitle("test")
        self.move(60, 60)
# 读取图片
        # self.frame = self.imgRead('26-03.jpg')
        
        
        # height, width, channel = self.frame.shape
        # bytesPerline = 3 * width
        # self.qImg = QImage(self.frame.data, width, height, QImage.Format_RGB888).rgbSwapped()
        # self.imgShow(self.frame, self.labelOrigin)
        
        
        # self.labelOrigin.setPixmap(QPixmap.fromImage(self.qImg))

# 各种控件
        self.btnOpenCamera = QPushButton('打开相机', self)
        self.btnOpenImage = QPushButton('打开图像', self)
        self.btnBinary = QPushButton('二值化', self)
        self.btnEdge = QPushButton('边缘检测', self)
        self.btnEdgeLine = QPushButton('提取边缘线', self)
        self.btnMedianLine = QPushButton('提取中值线', self)
        self.btnQuit = QPushButton('退出', self)
        
        self.labelOrigin = QLabel()
        self.labelBinary = QLabel()
        self.labelEdge = QLabel()
        self.labelEdgeLine = QLabel()
        self.labelMedianLine = QLabel()
        
        self.textBinary = QLineEdit(self)
        self.textBinary.setPlaceholderText("输入二值化阈值")
        # self.textBinary.resize(80, 40)
        self.textEdge = QLineEdit(self)
        self.textEdge.setPlaceholderText("输入Canny参数")
        
# 布局
        layout = QGridLayout(self)
        layout.addWidget(self.labelOrigin, 0, 1, 1, 2)
        layout.addWidget(self.labelBinary, 0, 3, 1, 2)
        layout.addWidget(self.labelEdge, 0, 5, 1, 2)
        layout.addWidget(self.labelEdgeLine, 3, 1, 1, 2)
        layout.addWidget(self.labelMedianLine, 3, 3, 1, 2)

        layout.addWidget(self.btnOpenCamera, 1, 1, 1, 1)
        layout.addWidget(self.btnOpenImage, 1, 2, 1, 1)
        layout.addWidget(self.btnBinary, 1, 4, 1, 1)
        layout.addWidget(self.btnEdge, 1, 6, 1, 1)
        layout.addWidget(self.btnEdgeLine, 4, 2, 1, 1)
        layout.addWidget(self.btnMedianLine, 4, 4, 1, 1)
        layout.addWidget(self.btnQuit, 4, 6, 1, 1)
        
        layout.addWidget(self.textBinary, 1, 3, 1, 1)
        layout.addWidget(self.textEdge, 1, 5, 1, 1)


        
    def initSlot(self):
# 按钮连接对应函数
        QtCore.QObject.connect(self.btnOpenCamera, QtCore.SIGNAL('clicked()'), self.openCamera)
        QtCore.QObject.connect(self.timerCamera, QtCore.SIGNAL('timeout()'), self.showCamera)
        QtCore.QObject.connect(self.btnOpenImage, QtCore.SIGNAL('clicked()'), self.imgRead)
        QtCore.QObject.connect(self.btnBinary, QtCore.SIGNAL('clicked()'), self.imgToBinary)
        QtCore.QObject.connect(self.btnEdge, QtCore.SIGNAL('clicked()'), self.imgToEdge)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL('clicked()'), self.close)

    '''this is the old style API老版本，会报错，但运行没问题
        self.btnOpenCamera.clicked.connect(self.openCamera)  
        self.timerCamera.timeout.connect(self.showCamera)        
        self.btnOpenImage.clicked.connect(self.imgRead)        
        self.btnBinary.clicked.connect(self.imgToBinary)
        self.btnEdge.clicked.connect(self.imgToEdge)    
        self.btnQuit.clicked.connect(self.close)
    '''

# 摄像头读取程序
    def openCamera(self):
        if self.timerCamera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            self.flagCamera = True
            if flag == False:
                msg = QMessageBox.warning(self, u'Warning', u'请检测相机与电脑是否连接正确')
            else:
                self.timerCamera.start(30)
                self.btnOpenCamera.setText(u'关闭相机')
        else:
            self.timerCamera.stop()
            self.cap.release()
            self.labelOrigin.clear()
            self.btnOpenCamera.setText(u'打开相机')
            
    def showCamera(self):
        flag, frame = self.cap.read()
        x, y = frame.shape[0:2]
        self.img = cv2.resize(frame, (int(y/4), int(x/4)))
        self.imgShow(self.img, self.labelOrigin)
        
        # flag, self.image = self.cap.read()
        # # face = self.face_detect.align(self.image)
        # # if face:
        # #     pass
        # show = cv2.resize(self.image, (640, 480))
        # show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # # print(show.shape[1], show.shape[0])
        # # show.shape[1] = 640, show.shape[0] = 480
        # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        # self.labelOrigin.setPixmap(QtGui.QPixmap.fromImage(showImage))

# 读取图片程序
    def imgRead(self, filename):
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', 
                                                   '*.png *.jpg *.bmp')
        if fileName is '':
            return
        img = cv2.imread(fileName, -1)
        if img.size == 1:
            return
        x,y = img.shape[0:2]
        self.img = cv2.resize(img, (int(y/8), int(x/8)))
        self.imgShow(self.img, self.labelOrigin)

# 图像显示在对应label上
    def imgShow(self, img, label):
        height, width = img.shape[0:2]
        # bytesPerline = width
        qImg = QImage(img.data, width, height, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(qImg))

# 二值图是单通道，把单通道值复制成三通道图，在Qt上正常显示(应该有更好的办法)
    def to3Channel(self, img):
        rows, columns = img.shape[0:2]
        npImg = np.array(img)
        tmp = np.ones((rows, columns), dtype='uint8')
        img3Channel = np.ones((rows, columns, 3), dtype='uint8')
        for i in range(3):
            img3Channel[:, :,i] = npImg * tmp
        return img3Channel


    def imgToBinary(self):
        binaryPar = int(self.textBinary.text())
        self.imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, self.imgBinary = cv2.threshold(self.imgGray, binaryPar, 255, cv2.THRESH_BINARY)
        
        imgBinToRGB = self.to3Channel(self.imgBinary)
        self.imgShow(imgBinToRGB, self.labelBinary)
        
    def imgToEdge(self):
        tmp = self.textEdge.text()
        cannyParLow, cannyParHigh = re.findall(r"\d+", tmp)
        cannyParLow = int(cannyParLow)
        cannyParHigh = int(cannyParHigh)
        self.imgEdge = cv2.Canny(self.imgGray, cannyParLow, cannyParHigh)
        imgEdgeToRGB = self.to3Channel(self.imgEdge)
        self.imgShow(imgEdgeToRGB, self.labelEdge)
        
    
# 退出按钮的处理
    def closeEvent(self, event):
        btnYes = QPushButton()
        btnCancel = QPushButton()
        msg = QMessageBox(QMessageBox.Warning, u'关闭', u'是否关闭？')
        msg.addButton(btnYes, QMessageBox.ActionRole)
        msg.addButton(btnCancel, QMessageBox.RejectRole)
        btnYes.setText(u'确定')
        btnCancel.setText(u'取消')
        if msg.exec_() == QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.flagCamera and self.cap.isOpened():
                self.cap.release()
            if self.timerCamera.isActive():
                self.timerCamera.stop()
            event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = windowImg()
    win.show()
    sys.exit(app.exec_())