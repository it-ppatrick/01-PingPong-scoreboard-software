from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from ControlBoard.ScoreModule.manager import ScoreManager
from ControlBoard.LifecycleModule.manager import LifecycleManager
from ControlBoard.SettingsModule.manager import SettingsManager

class MainControlBoard(QMainWindow):
    def __init__(self, engine, settings_store, triggers):
        """
        The Hub: Connects all isolated modules into one interface.
        engine: The MatchEngine (Logic).
        settings_store: The SettingsStore (Data).
        triggers: A dictionary of functions to update the Audience View.
        """
        super().__init__()
        self.setWindowTitle("Table Tennis Control - V02")
        self.setMinimumSize(450, 650)
        
        # 1. Central Widget & Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 2. Initialize Module Managers
        # We pass the shared 'engine' so every tab sees the same score.
        self.score_mod = ScoreManager(
            engine, 
            triggers['sync'], 
            self.show_win_confirmation # Internal trigger for the lifecycle popup
        )
        
        self.lifecycle_mod = LifecycleManager(
            engine, 
            self.score_mod.actions, # Link scoring to lifecycle for locking/unlocking
            triggers['live'], 
            triggers['standby'], 
            triggers['winner'], 
            triggers['sync']
        )
        
        self.settings_mod = SettingsManager(
            settings_store, 
            triggers['sync']
        )
        
        # 3. Assemble the Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.score_mod.get_widget(), "Live Scoring")
        self.tabs.addTab(self.lifecycle_mod.get_widget(), "Match Control")
        self.tabs.addTab(self.settings_mod.get_widget(), "Match Settings")
        
        self.main_layout.addWidget(self.tabs)

    def show_win_confirmation(self):
        """Management: When the engine detects a win, we switch tabs automatically."""
        self.tabs.setCurrentIndex(1) # Switch to 'Match Control' tab
        self.lifecycle_mod.ui.confirm_widget.show()
        self.score_mod.actions.match_active = False # Lock the scoring buttons