from backend.compile_cpp import compile_project
import subprocess


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
        self.ui.build_logs_widget.set_text("икщ вшв тще срфтпу еру лунищфкв дфнщге *ілгдд*")

        self.ui.ai_tab_layout.set_response_text("я найду тебя и разобью єбальнік")

    def build_task(self):
        self.ui.build_btn.setEnabled(False)
        self.ui.build_logs_widget.set_text("if there is no logs, it probably works")
        if self.ui.compiler_dropdown.currentText() == "C++ (default)":
            compile_project(self.project_path, self.ui.build_logs_widget)
        else:
            self.ui.build_logs_widget.set_text("this won't even be implemented, what's the point")
        self.ui.build_btn.setEnabled(True)

    def run_task(self):
        self.process = subprocess.Popen(["xterm", f"{self.project_path}/build/main"])

    def kill_task(self):
        try:
            self.process.terminate()  # Try to terminate first (more graceful)
            self.process.wait()  # Wait for the process to terminate
            self.process = None
        except AttributeError:
            print("Can't kill, maybe the process is already destroyed?")
