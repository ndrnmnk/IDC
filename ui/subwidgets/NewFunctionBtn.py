from PyQt5.QtWidgets import QPushButton, QGraphicsProxyWidget

from ui.windows.NewFunctionWindow import NewFunctionWindow


class NewFunctionBtn(QGraphicsProxyWidget):
    def __init__(self, parent_view):
        super().__init__()
        self.wv = parent_view
        self.btn = QPushButton("New function")
        self.btn.clicked.connect(self.on_click)

        self.setWidget(self.btn)

        parent_view.scene().addItem(self)
        self.setParentItem(parent_view.scene().menu)

    def on_click(self):
        NewFunctionWindow(self.wv)

    def suicide(self):
        try: self.deleteLater()
        except RuntimeError: pass