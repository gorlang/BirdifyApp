import sys
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import QMessageBox


class AudioDevices():
    """
    TODO improve error handling
    """
    def __init__(self, config):
        self._input_devices = QMediaDevices.audioInputs()
        self._output_devices = QMediaDevices.audioOutputs()

        self._selected_device_in = None
        self._selected_device_out = None

        self.priorityDevicesOut = config.DEVICE_NAMES_OUT
        self.priorityDevicesIn = config.DEVICE_NAMES_IN

        if not self._input_devices:
            QMessageBox.warning(None, "audio", "There is no audio input device available.")
            sys.exit(-1)

        if not self._output_devices:
            QMessageBox.warning(None, "audio", "There is no audio output device available.")
            sys.exit(-1)

          
    def getDevicesOut(self):
        devices = []
        for i, output_device in enumerate(self._output_devices):
            devices.append({"name": output_device.description(), "id": i, "type": "out"})
        return devices

    def getDevicesIn(self):
        devices = []
        for i, input_devices in enumerate(self._input_devices):
            devices.append({"name": input_devices.description(), "id": i, "type": "in"})
        return devices

    def selectDeviceIn(self, id):
        self._selected_device_in = id

    def selectDeviceOut(self, id):
        self._selected_device_out = id

    def selectedInput(self):
        return self._input_devices[self._selected_device_in]

    def selectedOutput(self):
        return self._output_devices[self._selected_device_out]

    def getExistingDeviceOut(self):
        for d in self.priorityDevicesOut:
            result = list(filter(lambda x: x["name"] == d, self.getDevicesOut()))
            if (len(result) > 0):
                break
        if len(result) > 0:
            self._selected_device_out = result[0]["id"]
            return self.selectedOutput()
        return None

    def getExistingDeviceIn(self):
        for d in self.priorityDevicesIn:
            print("d=", d)
            result = list(filter(lambda x: x["name"] == d, self.getDevicesIn()))
            if (len(result) > 0):
                break
        if len(result) > 0:
            self._selected_device_in = result[0]["id"]
            return self.selectedInput()
        return None


