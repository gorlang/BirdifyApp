import sys
from DetectorProcessThread import DetectorProcessThread
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

NUM_PASSES = 1
DEFAULT_RESULT_SIZE = 10

class DetectorProcessWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        print("DetectorProcessWidget().__init__")
        self.thread = DetectorProcessThread()
        self._result_size = DEFAULT_RESULT_SIZE
        self.thread.detect_result.connect(self.update_target)
        self._detect_counter = 0

    # This method must be implemented!
    def resizeEvent(self, event):
        self.thread.detect(self._result_size)

    def update_target(self, result):
        self._detect_counter += 1
        #print("update_target()-------", self._detect_counter)
        if result != None and len(result) > 0:
            data = result.split(",")
            if (len(data) > 0 and data[0] != ""):
                self._parent._result_table.insertData(0, data, None)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        layout = QVBoxLayout()
        self._result_table = ResultTable(["" for i in range(1,100)])
        self._detector = DetectorProcessWidget(self)
        self._button = QPushButton("Start Process")
        self._button.clicked.connect(lambda: self._detector.thread.detect(10))
        
        layout.addWidget(self._result_table)
        layout.addWidget(self._detector)
        layout.addWidget(self._button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == '__main__':

    print("__main__()")
    app = QApplication(sys.argv)
   
    main_win = MainWindow()
    main_win.setWindowTitle("DetectorThread()")
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 0.5
    main_win.resize(size, size)

    main_win.show()
    r = app.exec()
    main_win._detector.thread.stop()
    sys.exit(r)