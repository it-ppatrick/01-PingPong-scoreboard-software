from PyQt6.QtWidgets import QApplication

class DeployBroadcastAction:
    def __init__(self, ui, triggers):
        self.ui = ui
        self.triggers = triggers

    def execute(self):
        """Item 1: Handles logical deployment to physical monitors."""
        selected_row = self.ui.display_list.currentRow()
        
        if selected_row < 0:
            self.ui.flash_status("SELECT A DISPLAY FIRST")
            return
            
        if 'deploy' in self.triggers:
            self.triggers['deploy'](selected_row)
            self.ui.flash_status(f"BROADCAST LIVE ON SCREEN {selected_row}")