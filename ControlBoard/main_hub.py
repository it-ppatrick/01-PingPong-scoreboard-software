from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
# NEW IMPORT: Pointing to your revamped design file
from GUI_Design.control_board_revamp import ControlBoardUI 

from ControlBoard.ScoreModule.manager import ScoreManager
from ControlBoard.LifecycleModule.manager import LifecycleManager
from ControlBoard.SettingsModule.manager import SettingsManager

class MainControlBoard(QMainWindow):
    def __init__(self, engine, settings_store, triggers):
        super().__init__()
        self.setWindowTitle("Table Tennis Control - V02.20")
        self.setMinimumSize(450, 650)
        
        # 1. Initialize the NEW Revamped UI
        self.ui = ControlBoardUI()
        self.setCentralWidget(self.ui)
        
        # 2. Initialize Module Managers
        self.score_mod = ScoreManager(
            engine, 
            triggers['sync'], 
            self.show_win_confirmation 
        )
        
        # Use the engine from the Hub directly for Settings
        self.settings_mod = SettingsManager(
            engine,  # Pass engine to save settings directly
            triggers['sync']
        )
        
        self.lifecycle_mod = LifecycleManager(
            engine, 
            self.score_mod.actions, 
            triggers['live'], 
            triggers['standby'], 
            triggers['winner'], 
            triggers['sync']
        )

        # 3. Connect the Revamped UI to the Managers
        self.setup_revamp_connections(triggers)

    def setup_revamp_connections(self, triggers):
        """Bridge the Revamped UI buttons to the Manager logic."""
        
        # Scoring Buttons -> Score Module Actions
        self.ui.p1_add.clicked.connect(lambda: self.score_mod.actions.execute(1, "add"))
        self.ui.p2_add.clicked.connect(lambda: self.score_mod.actions.execute(2, "add"))
        self.ui.p1_minus.clicked.connect(lambda: self.score_mod.actions.execute(1, "undo"))
        self.ui.p2_minus.clicked.connect(lambda: self.score_mod.actions.execute(2, "undo"))
        
        # Settings Page -> Settings Manager
        # We link the 'Apply' button to our status flash logic
        self.ui.apply_settings_btn.clicked.connect(self.handle_apply_settings)
        
        # Broadcast Button -> Lifecycle Manager
        self.ui.broadcast_btn.clicked.connect(triggers['live'])
        self.ui.broadcast_btn.clicked.connect(lambda: self.ui.flash_status("BROADCAST LIVE"))

    def handle_apply_settings(self):
        """Executes the save and triggers your 5-second green feedback."""
        # Map the UI inputs to the engine via the manager
        self.settings_mod.apply_from_revamp(self.ui) 
        self.ui.flash_status("SETTINGS APPLIED")

    def show_win_confirmation(self):
        """Management: Automatically switch to the Scoring tab and show win logic."""
        self.ui.stack.setCurrentIndex(0) # Keep them on scoring to see the result
        self.ui.flash_status("WIN DETECTED - CHECK CONTROLS")
        self.score_mod.actions.match_active = False