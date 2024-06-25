
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit
import sys
from mainWindow import Ui_MainWindow
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt6.QtGui import QPixmap, QColor, QImage
import numpy as np

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)


class Main(QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self, *args, **kwargs)

        self.video = VideoThread()
        self.video.change_pixmap_signal.connect(self.update_image)
        self.video.start()

        self.captureButton.clicked.connect(self.capture_image)
    def update_image(self, cv_img):
            """Updates the image_label with a new opencv image"""
            qt_img = self.convert_cv_qt(cv_img)
            self.videoDisplay.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
            """Convert from an opencv image to QPixmap"""
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.videoDisplay.width(), self.videoDisplay.height(), Qt.AspectRatioMode.KeepAspectRatio)
            
            return QPixmap.fromImage(p)

    def capture_image(self):
        current_pixmap = self.videoDisplay.pixmap() 
        self.imageDisplay.setPixmap(current_pixmap)



#  https://github.com/ivan-alles/localizer for neural net object orientation and position detection from a video feed.



if __name__ == '__main__':
    app  = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())