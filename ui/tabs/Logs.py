from PyQt5.QtWidgets import QTextBrowser, QVBoxLayout


class BuildLogsTabLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.logs_text_widget = QTextBrowser()
        self.addWidget(self.logs_text_widget)

    def set_text(self, text):
        self.logs_text_widget.setText(text)

    def append(self, text):
        self.logs_text_widget.append(text)
