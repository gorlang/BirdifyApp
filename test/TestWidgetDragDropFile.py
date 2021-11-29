import sys, os
sys.path.append('src')
from PySide6.QtWidgets import QApplication, QListWidgetItem, QMainWindow
from WidgetDragDropFile import WidgetDragDropFile
from PySide6 import QtGui
from AppConfig import AppConfig


class MainForm(QMainWindow):
    # def __init__(self, parent=None):
    #    super(MainForm, self).__init__(parent)
    def __init__(self, parent):
        super().__init__()
        self._config = parent._config
        self.view = WidgetDragDropFile(self)
        self.view.fileDropped.connect(self.fileDropped)
        self.setCentralWidget(self.view)

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print("url=", url)
                icon_path = self._config.BASE_PATH + "icons/" + self._config.ICONS[self._config.BUTTON_IMPORT]
                icon = QtGui.QIcon(icon_path)
                filename = url.split("/")[-1]
                print("filename= ", filename)
                item = QListWidgetItem(filename, self.view)  # url
                print("item.text()", item.text())
                item.setIcon(icon)
                item.setStatusTip(url)

class MockParent():
    def __init__(self):
        self._config = AppConfig()

def main():
    
    app = QApplication(sys.argv)
    form = MainForm(MockParent())
    form.show()
    app.exec()

if __name__ == '__main__':
    main()