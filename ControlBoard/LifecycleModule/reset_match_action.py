from PyQt6.QtWidgets import QMessageBox

class ResetMatchAction:
    def __init__(self, ui, engine, triggers, sync_hub_callback):
        self.ui = ui
        self.engine = engine
        self.triggers = triggers
        self.sync_hub = sync_hub_callback

    def execute(self, is_flipped):
        """Issue 3: Asks user if they want to reset player names along with scores."""
        msg = QMessageBox(self.ui)
        msg.setWindowTitle("Start New Match")
        msg.setText("Do you want to reset everything?")
        msg.setInformativeText("Click 'Yes' to reset scores and names.\nClick 'No' to reset scores only.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        ret = msg.exec()
        if ret == QMessageBox.StandardButton.Cancel: return False

        self.engine.reset_full_match()
        
        if ret == QMessageBox.StandardButton.Yes:
            self.engine.p1_name, self.engine.p2_name = "PLAYER 1", "PLAYER 2"
            self.ui.p1_name_display.setText("PLAYER 1")
            self.ui.p2_name_display.setText("PLAYER 2")
            self.ui.p1_input.clear()
            self.ui.p2_input.clear()

        self.sync_hub(is_flipped)
        self.triggers['sync']()
        self.triggers['standby']() 
        return True # Signal that reset was completed