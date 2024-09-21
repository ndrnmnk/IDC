from PyQt5.QtWidgets import QTextBrowser, QVBoxLayout


def create_build_logs_tab():
    layout = QVBoxLayout()

    text_widget = QTextBrowser()
    text_widget.setText("blablablablabla")

    layout.addWidget(text_widget)
    return layout
