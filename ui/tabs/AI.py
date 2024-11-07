from PyQt5.QtWidgets import QTextBrowser, QLineEdit, QVBoxLayout


class AiTabLayout(QVBoxLayout):
	def __init__(self):
		super().__init__()
		self.response_widget = QTextBrowser()

		self.request_widget = QLineEdit()
		self.request_widget.setPlaceholderText("Question to AI")

		self.addWidget(self.response_widget)
		self.addWidget(self.request_widget)

	def get_request_text(self):
		self.request_widget.setText('')
		print(self.request_widget.text())

	def set_response_text(self, text):
		self.response_widget.setText(text)