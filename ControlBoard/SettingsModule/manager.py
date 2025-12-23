from ControlBoard.SettingsModule.apply_settings_action import ApplySettingsAction

class SettingsManager:
    def __init__(self, engine, sync_callback):
        """
        Manages the transition of data from the UI to the Logic Engine.
        engine: The MatchEngine instance.
        sync_callback: The function that updates the Audience UI.
        """
        self.engine = engine
        self.sync_callback = sync_callback
        # We keep a reference to the action class for organizational logic
        self.apply_action = None 

    def apply_from_revamp(self, ui):
        """
        Maps the inputs from the Revamped UI to the MatchEngine.
        This follows the 'Best of' and 'Points' logic from your design.
        """
        # 1. Update Player Names
        self.engine.p1_name = ui.p1_input.text().upper() or "PLAYER 1"
        self.engine.p2_name = ui.p2_input.text().upper() or "PLAYER 2"
        
        # 2. Update Points per Set (Radio Button Logic)
        if ui.pts_11.isChecked():
            self.engine.pts_limit = 11
        else:
            self.engine.pts_limit = 21
            
        # 3. Update Series Length (Match Format Logic)
        if ui.best_1.isChecked():
            self.engine.match_limit = 1
        elif ui.best_3.isChecked():
            self.engine.match_limit = 3
        elif ui.best_5.isChecked():
            self.engine.match_limit = 5
            
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