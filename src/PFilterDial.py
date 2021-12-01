from PySide6.QtWidgets import QDial

class PFilterDial(QDial):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setRange(0, 100)
        self.setSingleStep(1)
        self._text = self._parent._config.DIAL_FILTER_P
        self._parent._label_filter_dial.setText(self._text + "=" + str(self._parent._filter_p))

        self.valueChanged.connect(self.value_changed)
        self.sliderMoved.connect(self.slider_position)
        self.sliderPressed.connect(self.slider_pressed)
        self.sliderReleased.connect(self.slider_released)

    def value_changed(self, i):
        self._parent._filter_p = i/100
        p_display = round(self._parent._filter_p, 2)
        self._parent._label_filter_dial.setText(self._text + "=" + str(p_display))

    def slider_position(self, p):
        pass

    def slider_pressed(self):
        pass

    def slider_released(self):
        pass