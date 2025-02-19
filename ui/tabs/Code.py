from PyQt5.QtWidgets import QGridLayout
from ui.widgets.CodingGraphicsScene import WorkspaceView


class CodeTabLayout(QGridLayout):
	def __init__(self):
		super().__init__()
		self.setColumnStretch(0, 4)

		self.view = WorkspaceView()

		self.addWidget(self.view, 0, 0)

		json1 = {
			"shape": 0,
			"pos": [20, 20],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"dropdown": ["hgfghgfghgfghgf", "run"]},
					{"text": "whatever"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				],
				[
					{"text": "if"},
					{"bool_entry": "0"}
				],
				[
					{"text": "elif"},
					{"bool_entry": "0"}
				],
				[
					{"text": "else"}
				],
				[
					{"text": "why do you need so much layers"}
				]
			]}

		json2 = {
			"shape": 0,
			"pos": [20, 300],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "Move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				]
			]}

		json3 = {
			"shape": 0,
			"pos": [20, 600],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				],
				[
					{"text": "if"},
					{"bool_entry": "0"}
				],
				[
					{"text": "elif"},
					{"bool_entry": "0"}
				],
				[
					{"text": "else"}
				],
				[
					{"text": "why do you need so much layers"}
				]
			]}

		json4 = {
			"shape": 0,
			"pos": [20, 900],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "Move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				]
			]}

		json5 = {
			"shape": 2,
			"pos": [20, 1200],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				],
				[
					{"text": "if"},
					{"bool_entry": "0"}
				],
				[
					{"text": "elif"},
					{"bool_entry": "0"}
				],
				[
					{"text": "else"}
				],
				[
					{"text": "why do you need so much layers"}
				]
			]}

		json6 = {
			"shape": 2,
			"pos": [20, 1500],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "Move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				]
			]}

		json7 = {
			"shape": 3,
			"pos": [20, 1800],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				],
				[
					{"text": "икщ ащкпще ещ срфтпу еру лунищфкв дфнщге *ісгдд*"}
				]
			]}

		json8 = {
			"shape": 3,
			"pos": [20, 2100],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "Move"},
					{"int_entry": "10"},
					{"text": "steps to"},
					{"text_entry": "WW3"},
					{"text": "that will begin in"},
					{"bool_entry": "0"}
				]
			]}

		json9 = {
			"shape": 1,
			"pos": [20, 2400],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text": "hhhhhhhhhhhhhhhhhhhhhhhhh"}
				]
			]}

		json10 = {
			"shape": 0,
			"pos": [20, 2700],
			"internal_name": "move_n_steps",
			"color": "#888888",
			"data": [
				[
					{"text_entry": "text entry only?"}
				],
				[
					{"text": "no, there is a second layer."}
				]
			]}

		self.view.add_blocks([json1, json2, json3, json4, json5, json6, json7, json8, json9, json10])
