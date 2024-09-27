from PyQt5.QtWidgets import QTextBrowser, QVBoxLayout


"""
def create_build_logs_tab():
    layout = QVBoxLayout()

    text_widget = QTextBrowser()
    text_widget.setText("blablablablabla")

    layout.addWidget(text_widget)
    return layout
"""

class BuildLogsTabLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        logs_text_widget = QTextBrowser()
        logs_text_widget.setText("икщ вшв тще срфтпу еру лунищфкв дфнщге *ілгдд*")
        self.addWidget(logs_text_widget)