import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings, QThread, pyqtSignal
import subprocess
import json


class CommandRunner(QThread):
	# create signals
	output_signal = pyqtSignal(str)
	finished_signal = pyqtSignal()

	def __init__(self, command, logs_widget):
		super().__init__()
		self.command = command
		self.logs_widget = logs_widget
		self.process = None  # store the process here

	def run(self):
		# run the command
		self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

		# read output and emmit signals to update logs_widget
		for line in self.process.stdout:
			self.output_signal.emit(line)

		# same for errors
		for line in self.process.stderr:
			self.output_signal.emit(line)

		self.process.stdout.close()
		self.process.stderr.close()
		self.process.wait()

		self.finished_signal.emit()

	# def terminate_process(self):
	#     if self.process and self.process.poll() is None:  # if it's running, kill it
	#         self.process.kill()
	#         self.process.wait()
	#         self.finished_signal.emit()  # and re-enable buttons :)


class Backend:
	def __init__(self, ui):
		self.ui = ui

		# example sprite list content
		self.ui.spritelist.add_item('Main', 'Generic class')
		self.ui.spritelist.add_item('test class', 'Hello, World!')
		self.ui.spritelist.currentItemChanged.connect(self.ui.code_tab.sprite_manager.change_current_sprite)

		for item in self.ui.spritelist.item_meta:
			self.ui.code_tab.sprite_manager.all_sprite_code[item[0]] = {"instance_of": item[1], "code": {}, "roots": [], "vars": {}}

		# example sounds list content
		self.ui.sounds_tab_layout.add_sound("error", "textures/images/error.png")

		# example textures list content
		self.ui.textures_tab_layout.add_texture("error", "textures/images/error.png")
		self.ui.textures_tab_layout.add_texture("warning", "textures/images/warning.png")
		self.ui.textures_tab_layout.add_texture("logo", "textures/images/logo.png")
		self.ui.textures_tab_layout.add_texture("test", "textures/images/test.png")

		# example build logs tab content
		self.ui.logs_widget.set_text("икщ вшв тще срфтпу еру лунищфкв дфнщге *ілгдд*")

		self.ui.ai_tab_layout.set_response_text("Press Alt+F4 for me to fix everything instantly")

		self.runner = None

	def get_build_command(self, run=0):
		for json_obj in self.ui.compilers:
			if json_obj == self.ui.compiler_dropdown.currentText():
				if run:
					return self.ui.compilers[json_obj]["run"]
				return self.ui.compilers[json_obj]["command"]
		return None  # return None if not found

	def run_command(self, command):
		if self.runner and self.runner.isRunning():
			self.ui.logs_widget.append("A new command added to the queue")
			self.runner.finished_signal.connect(lambda c=command: self.run_command(c))
			return
		self.runner = CommandRunner(command, self.ui.logs_widget)

		# connect the signals to update logs_widget and to enable buttons
		self.runner.output_signal.connect(lambda text: self.ui.logs_widget.append(text))

		# Start the thread to run the command in the background
		self.runner.start()

	def closeEvent(self, event):
		# ensure that the thread finished before the application closed
		if self.runner is not None:
			self.runner.wait()  # blocks until process finishes
		event.accept()

	def verify_close(self):
		reply = QMessageBox.warning(self.ui, "IDC: Exit", "Save the project before exit?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
		if reply == QMessageBox.Cancel:
			return False
		if reply == QMessageBox.Yes:
			self.save_project()
			return True
		else:
			return True

	def open_project(self, no_load=False):
		if not self.ui.opened_project_path:
			settings = QSettings()
			last_path = settings.value("lastFilePath", defaultValue=".")
			file_path, _ = QFileDialog.getOpenFileName(None, "Select a File", last_path, "IDC Project (*.idcp)")
			if not file_path:
				return
			settings.setValue("lastFilePath", QFileDialog().directory().absolutePath())

			self.ui.opened_project_path = os.path.dirname(file_path)
			for addon in self.ui.addons_manager.addons_names:
				self.ui.addons_manager.addons[addon].on_open_project()
			if not no_load:
				with open(file_path) as f:
					data = json.load(f)
				self.ui.code_tab.sprite_manager.all_sprite_code = data
				self.ui.code_tab.var_manager.on_load_project()
				self.ui.code_tab.sprite_manager.show_sprite("Main")
				self.ui.spritelist.remove_all()
				for item in data:
					if item == "vars":
						continue
					self.ui.spritelist.add_item(item, data[item]["instance_of"])
		else:
			reply = QMessageBox.question(self.ui, "IDC warning", "Save current project before continuing?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
			if reply == QMessageBox.Yes:
				self.save_project()
			if reply != QMessageBox.Cancel:
				self.ui.opened_project_path = None
				self.open_project()

	def save_project(self):
		for addon in self.ui.addons_manager.addons_names:
			self.ui.addons_manager.addons[addon].on_save_project()
		if not self.ui.opened_project_path:
			self.open_project(True)
		print(self.ui.opened_project_path)
		full_project_path = os.path.join(self.ui.opened_project_path, "Project.idcp")
		with open(full_project_path, 'w', encoding='utf-8') as f:
			json.dump(self.ui.code_tab.get_project_data(), f, ensure_ascii=False, indent=4)

