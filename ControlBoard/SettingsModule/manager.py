from GUI_Design.settings_ui import SettingsUI
from ControlBoard.SettingsModule.apply_settings_action import ApplySettingsAction

class SettingsManager:
    def __init__(self, settings_store, sync_callback):
        self.ui = SettingsUI()
        self.apply_action = ApplySettingsAction(self.ui, settings_store, sync_callback)
        self.ui.apply_btn.clicked.connect(self.apply_action.execute)

    def get_widget(self):
        return self.ui