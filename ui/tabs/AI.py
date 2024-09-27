from PyQt5.QtWidgets import QTextBrowser, QLineEdit, QVBoxLayout


class AiTabLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        response_widget = QTextBrowser()
        response_widget.setText("я найду тебя и разобью єбальнік")

        request_widget = QLineEdit()
        request_widget.setPlaceholderText("Question to AI")

        self.addWidget(response_widget)
        self.addWidget(request_widget)
