from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QSizePolicy
from PyQt5 import uic , QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
from ultralytics import YOLO
import icons.icons_rc


class Predict(QMainWindow):
    def __init__(self):
        super(Predict, self).__init__()
        uic.loadUi('./predictUI.ui', self)

        # remove windows title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # set main background transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # button clicks on top bar
        # minimize window
        self.btnMinus.clicked.connect(self.showMinimized)
        # Close window
        self.btnClose.clicked.connect(self.close)

        # Load a model
        self.model = YOLO("./runs/classify/train2/weights/best.pt")  # load a pretrained model

        # upload btn func
        self.btnUpload.clicked.connect(self.upload)
        self.btnPredict.clicked.connect(self.predict)

        self.imgPath = ''


    def upload(self):
        # Create custom QFileDialog
        dialog = QFileDialog()

        # Set filter for PNG and JPG files
        dialog.setNameFilters(["PNG Files (*.png);;JPG Files (*.jpg)"])

        # Show dialog and get selected file
        if dialog.exec_():
            file_path = dialog.selectedFiles()[0]

            # Open and display the image
            pixmap = QPixmap(file_path)
            self.imgPath = file_path
            label = self.lblImage
            label.setPixmap(pixmap)

            # Set scaled contents and size policy
            label.setScaledContents(True)
            label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

            # Scale pixmap to fit within label dimensions
            width = label.width()
            height = label.height()
            scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
            label.setPixmap(scaled_pixmap)


    def predict(self):
        results = self.model.predict(str(self.imgPath), save=True)
        top1 = results[0].probs.top1
        predict = str(results[0].names[top1])

        if predict == "airplane":
            predict = "هواپیما"
        elif predict == "automobile":
            predict = "ماشین"
        elif predict == "cat":
            predict = "گربه"
        elif predict == "dog":
            predict = "سگ"
        elif predict == "deer":
            predict = "گوزن"
        elif predict == "bird":
            predict = "پرنده"
        elif predict == "frog":
            predict = "غورباقه"
        elif predict == "horse":
            predict = "اسب"
        elif predict == "ship":
            predict = "کشتی"
        elif predict == "truck":
            predict = "تراکتور"

        self.lblResult.setText(predict)

    #main window drag funcs
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = Predict()
    UIWindow.show()
    app.exec_()