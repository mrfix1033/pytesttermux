from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PIL import Image, ImageDraw
from math import ceil

# scale
s = 2.0
# minimum sensitive slider
min_sensitive = 1

# constants
big_circle = ceil(0 * s), ceil(0 * s), ceil(100 * s), ceil(100 * s)
size_eye = ceil(15 * s), ceil(15 * s)
first_eye = ceil(20 * s), ceil(20 * s), *size_eye
second_eye = ceil(65 * s), ceil(20 * s), *size_eye
rot = ceil(20 * s), ceil(30 * s), ceil(60 * s), ceil(50 * s)


def multiply_geometry(geometry, multiplier):
    ret = []
    for i in geometry:
        ret.append(ceil(i * multiplier))
    return ret


def geometry_to_points(geometry):
    return minus_one_from_end_points((tuple(geometry[:2]),
                                     (geometry[2] + geometry[0], geometry[3] + geometry[1])))

def minus_one_from_end_points(points):
    p2 = [points[0], []]
    for i in points[1]:
        p2[1].append(i - 1)
    p2[1] = tuple(p2[1])
    return p2


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)

        def a(e=None):
            final_s = min_sensitive + self.verticalSlider.value()
            big_circle_c = multiply_geometry(big_circle, final_s)
            first_eye_c = multiply_geometry(first_eye, final_s)
            second_eye_c = multiply_geometry(second_eye, final_s)
            rot_c = multiply_geometry(rot, final_s)
            im = Image.new('RGBA', big_circle_c[2:])
            draw = ImageDraw.Draw(im)
            for i in big_circle_c, first_eye_c, second_eye_c:
                draw.ellipse(geometry_to_points(i), outline=(255, 0, 0))
            draw.arc(geometry_to_points(rot_c), 5, 175, (255, 0, 0))
            # save image
            im.save('im.png')
            # adjust label size
            self.label.setGeometry(0, 0, *big_circle_c[:2])
            # open and set image
            self.label.setPixmap(QPixmap('im.png'))

        self.verticalSlider.changeEvent = a
        a()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.verticalSlider.setSizePolicy(sizePolicy)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridLayout.addWidget(self.verticalSlider, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 365, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.excepthook = lambda cls, exception, traceback: sys.__excepthook__(cls, exception, traceback)
sys.exit(app.exec())
