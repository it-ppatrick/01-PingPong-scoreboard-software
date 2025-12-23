class ApplySettingsAction:
    def __init__(self, ui, engine, sync_callback):
        self.ui = ui
        self.engine = engine
        self.sync_callback = sync_callback

    def execute(self):
        # 1. Update Names
        self.engine.p1_name = self.ui.p1_input.text() or "PLAYER 1"
        self.engine.p2_name = self.ui.p2_input.text() or "PLAYER 2"

        # 2. Update Match Limit (Parse "Best of 3" -> 3)
        selection = self.ui.match_limit_box.currentText()
        # We take the last character of the string and turn it into an integer
        self.engine.match_limit = int(selection.split(" ")[-1])

        # 3. Refresh the displays
        self.sync_callback()
        print(f"Settings Applied: {self.engine.p1_name} vs {self.engine.p2_name} ({selection})")