from PyQt5.QtWidgets import QPushButton, QGraphicsProxyWidget

from ui.windows.NewVariableWindow import NewVariableWindow


class NewVariableBtn(QGraphicsProxyWidget):
    def __init__(self, parent_view):
        super().__init__()
        self.wv = parent_view
        self.btn = QPushButton("New variable")
        self.btn.clicked.connect(self.on_click)

        self.setWidget(self.btn)

        parent_view.scene().addItem(self)
        self.setParentItem(parent_view.scene().menu)

    def on_click(self):
        NewVariableWindow(self.wv)

    def suicide(self):
        try:
            self.deleteLater()
        except RuntimeError:
            pass