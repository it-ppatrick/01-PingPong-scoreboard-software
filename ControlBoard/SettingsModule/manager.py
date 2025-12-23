from ControlBoard.SettingsModule.apply_settings_action import ApplySettingsAction

class SettingsManager:
    def __init__(self, engine, sync_callback):
        self.engine = engine
        self.sync_callback = sync_callback

    def apply_from_revamp(self, ui):
        """Reads Radio Buttons and LineEdits to update the Engine."""
        # Names
        self.engine.p1_name = ui.p1_input.text().upper() or "PLAYER 1"
        self.engine.p2_name = ui.p2_input.text().upper() or "PLAYER 2"
        
        # Points Logic
        self.engine.pts_limit = 11 if ui.pts_11.isChecked() else 21
            
        # Series Logic
        if ui.best_1.isChecked(): self.engine.match_limit = 1
        elif ui.best_3.isChecked(): self.engine.match_limit = 3
        elif ui.best_5.isChecked(): self.engine.match_limit = 5
            
        self.sync_callback()
            
        # 4. Trigger the UI Refresh
        self.sync_callback()
        
        # Internal Debugging
        print(f"Engine Updated: {self.engine.pts_limit} pts, Best of {self.engine.match_limit}")

    def get_widget(self):
        """
        Note: In V02.20, the Hub manages the Revamp UI directly. 
        This method is kept for legacy compatibility if needed.
        """
        return None