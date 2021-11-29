import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from PySide6.QtWidgets import QListWidget

def getMonthNameFromWeek(week):
    year = dt.now().year
    date = datetime.date(year, 1, 1) + relativedelta(weeks=+week)
    return date.strftime("%b")

class ListWidgetWeeks(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._weeks = [f"{getMonthNameFromWeek(w)}, week={str(w)}" for w in range(1,53)]
        self.addItems(self._weeks)
        self.item(self._parent._current_week-1).setSelected(True)
        self.currentItemChanged.connect(self.index_changed)
        self.currentTextChanged.connect(self.text_changed)

    def index_changed(self, item):
        pass

    def text_changed(self, item):
        selected_week = item.split("=")[1]
        self._parent._week = selected_week
        self._parent.updateSettings()