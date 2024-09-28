class Backend:
    def __init__(self, ui):
        self.ui = ui

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
