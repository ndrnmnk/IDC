

class BaseAddon:
	def __init__(self, ui):
		self.ui = ui
		self.init()

	def init(self):
		pass

	def on_open_project(self):
		pass

	def on_save_project(self):
		pass

	def on_compile(self):
		pass

	def on_run(self):
		pass

	def on_kill(self):
		pass

	def on_compiler_options(self):
		pass

	def on_options(self):
		pass

	def on_idc_close(self):
		pass

	def on_delete(self):
		return True

	def on_install(self):
		pass

	def on_update(self):
		pass
