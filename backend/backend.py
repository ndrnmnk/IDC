from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


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

		self.process = None
		self.project_path = "/home/andrey/IDC-COMPILE-TEST"
		# bind actions to buttons
		self.ui.build_btn.pressed.connect(self.build_task)
		self.ui.run_btn.pressed.connect(self.run_task)
		self.ui.kill_btn.pressed.connect(self.kill_task)

		# example sprite list content
		self.ui.spritelist.add_item('Cat', '2D Sprite')
		self.ui.spritelist.add_item('Dialog window', 'UI')
		self.ui.spritelist.add_item('Cube', '3D Sprite')

		# example problems tab content
		self.ui.problems_tab.add_item(0, 'warning')
		self.ui.problems_tab.add_item(0, 'warning')
		self.ui.problems_tab.add_item(1, 'error')

		# example sounds list content
		self.ui.sounds_tab_layout.add_sound("error", "textures/error.png")

		# example textures list content
		self.ui.textures_tab_layout.add_texture("error", "textures/error.png")
		self.ui.textures_tab_layout.add_texture("warning", "textures/warning.png")
		self.ui.textures_tab_layout.add_texture("logo", "textures/logo.png")
		self.ui.textures_tab_layout.add_texture("test", "textures/test.png")

		# example build logs tab content
		self.ui.logs_widget.set_text("икщ вшв тще срфтпу еру лунищфкв дфнщге *ілгдд*")

		self.ui.ai_tab_layout.set_response_text("я найду тебя и разобью єбальнік")

		self.runner = None

	def build_task(self):
		print(self.project_path)
		self.set_buttons_state(False)
		command = self.get_build_command().format(f"{self.project_path}")
		self.run_command(command, self.ui.logs_widget)

	def run_task(self):
		self.set_buttons_state(False)
		command = self.get_build_command(run=1).format(f"{self.project_path}")
		self.run_command(command, self.ui.logs_widget)

	def kill_task(self):
		if self.runner:
			self.runner.terminate_process()

	def get_build_command(self, run=0):
		for json_obj in self.ui.compilers:
			if json_obj == self.ui.compiler_dropdown.currentText():
				if run:
					return self.ui.compilers[json_obj]["run"]
				return self.ui.compilers[json_obj]["command"]
		return None  # return None if not found

	def run_command(self, command, logs_widget):
		self.runner = CommandRunner(command, logs_widget)

		# connect the signals to update logs_widget and to enable buttons
		self.runner.output_signal.connect(lambda text: logs_widget.append(text))
		self.runner.finished_signal.connect(self.set_buttons_state)

		# Start the thread to run the command in the background
		self.runner.start()

	def closeEvent(self, event):
		# ensure that the thread finished before the application closed (chatgpt ahh comment)
		if self.runner is not None:
			self.runner.wait()  # blocks until process finishes
		event.accept()

	def set_buttons_state(self, state=True):
		self.ui.build_btn.setEnabled(state)
		self.ui.run_btn.setEnabled(state)
		self.ui.kill_btn.setEnabled(not state)
