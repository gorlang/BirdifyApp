from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QMessageBox, QVBoxLayout, QWidget
from BLabel import BLabel
from ListWidgetLangs import ListWidgetLangs
from ListWidgetWeeks import ListWidgetWeeks

class WidgetSettings(QWidget):
    def __init__(self, parent):
        super().__init__()    
        layout = QVBoxLayout()

        self._parent = parent
        self.msg = "Audio needs to be running to start detection!"

        layout.addWidget(BLabel("Week", 14))
        layout.addWidget(ListWidgetWeeks(parent))

        layout.addWidget(BLabel("Language", 14))
        layout.addWidget(ListWidgetLangs(parent))

        # Audio status

        layout.addWidget(BLabel("Audio", 14))

        audio_on = self._parent._app_controller._audio_on
        check_state_audio = Qt.Checked if audio_on else Qt.Unchecked
        audioStatus = QCheckBox("Audio Enabled")
        audioStatus.setCheckState(check_state_audio)
        audioStatus.stateChanged.connect(self.toggleAudio)
        layout.addWidget(audioStatus)
        
        # Detect status

        layout.addWidget(BLabel("Detection", 14))

        detect_on = self._parent._app_controller._detection_on
        check_state_detect = Qt.Checked if detect_on else Qt.Unchecked
        self.detectionStatus = QCheckBox("Detection Enabled")
        self.detectionStatus.setCheckState(check_state_detect)
        self.detectionStatus.stateChanged.connect(self.toggleDetection)
        self.disableDetectCheckBox(not audio_on)
        layout.addWidget(self.detectionStatus)
       
        layout.addWidget(BLabel(self.msg, 12))
        self.setLayout(layout)

    def toggleAudio(self, i):
        checked = False if i == 0 else True
        print("toogleAudio(), checked=", checked)
        audio_on = self._parent._app_controller._audio_on
        if not checked:
            if audio_on:
                print("set audio off!")
                self.disableDetectCheckBox()
                self._parent._app_controller.stopDetection()
                self.detectionStatus.setCheckState(QtCore.Qt.CheckState(False))
                self._parent._app_controller.stopAudio()
        else:
            if not audio_on:
                print("set audio on!")
                self._parent._app_controller.startAudio()
                self.disableDetectCheckBox(False)
                #self._parent._app_controller.startDetection()
                #self.detectionStatus.setCheckState(QtCore.Qt.CheckState(True))


    def disableDetectCheckBox(self, disableflag=True):
        self.detectionStatus.setDisabled(disableflag)

    def toggleDetection(self, i):

        checked = False if i == 0 else True
        detection_on = self._parent._app_controller._detection_on
        audio_on = self._parent._app_controller._audio_on

        if checked:
            if not detection_on and audio_on:
                print("start detection!")
                self._parent._app_controller.startDetection()
            else:
                QMessageBox.warning(None, "", self.msg)
                self.detectionStatus.setCheckState(QtCore.Qt.CheckState(False))
        else:
            if detection_on:
                print("stop detection!")
                self._parent._app_controller.stopDetection()
