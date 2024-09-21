from PyQt5.QtWidgets import QTextBrowser, QLineEdit, QVBoxLayout


def create_ai_tab():
    layout = QVBoxLayout()

    response_widget = QTextBrowser()
    response_widget.setText("я найду тебя и разобью єбальнік")

    request_widget = QLineEdit()
    request_widget.setPlaceholderText("Question to AI")

    layout.addWidget(response_widget)
    layout.addWidget(request_widget)
    return layout
