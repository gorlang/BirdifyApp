from PySide6.QtWidgets import QDial

class PFilterDial(QDial):
    def __init__(self, parent, parent_widget):
        super().__init__()

        self._parent = parent
        self._parent_widget = parent_widget

        self._text = self._parent._config.DIAL_FILTER_P

        # differentiate behavior
        self._p_widget = True if self._parent_widget._filter_p != None else False

        p_filter = self._parent_widget._filter_p if self._p_widget else self._parent._filter_p
        parent_widget._label_filter_dial.setText(self._text + "=" + str(p_filter))

        self.setRange(0, 100)
        self.setSingleStep(1)
        self.setValue(int(p_filter * 100))

        self.valueChanged.connect(self.value_changed)
        self.sliderMoved.connect(self.slider_position)
        self.sliderPressed.connect(self.slider_pressed)
        self.sliderReleased.connect(self.slider_released)

    def value_changed(self, i):
        p_filter = i/100
        if self._p_widget:
            self._parent_widget._filter_p = p_filter
        else:
            self._parent._filter_p = p_filter
        p_display = round(p_filter, 2)
        self._parent_widget._label_filter_dial.setText(self._text + "=" + str(p_display))

    def slider_position(self, p):
        pass

    def slider_pressed(self):
        pass

    def slider_released(self):
        pass