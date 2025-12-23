from PyQt6.QtWidgets import QMainWindow
from GUI_Design.control_board_revamp import ControlBoardUI 
from ControlBoard.ScoreModule.manager import ScoreManager
from ControlBoard.LifecycleModule.manager import LifecycleManager
from ControlBoard.SettingsModule.manager import SettingsManager
from ControlBoard.BroadcastModule.manager import BroadcastManager

class MainControlBoard(QMainWindow):
    def __init__(self, engine, settings_store, triggers):
        super().__init__()
        self.setWindowTitle("Table Tennis Control - V02.20")
        self.setMinimumSize(450, 650)
        self.triggers = triggers 
        self.is_flipped = False
        self.match_started = False 

        # 1. UI Initialization
        self.ui = ControlBoardUI()
        self.setCentralWidget(self.ui)
        
        # 2. Manager Initialization
        self.score_mod = ScoreManager(engine, triggers['sync'], self.show_win_confirmation)
        self.settings_mod = SettingsManager(engine, triggers['sync'])
        self.broadcast_mod = BroadcastManager(self.ui, triggers)
        self.lifecycle_mod = LifecycleManager(
            engine, self.score_mod.actions, self.ui, triggers, self.refresh_hub_scores
        )

        # 3. Connections
        self.setup_revamp_connections()
        self.ui.set_scoring_enabled(False) 
        self.refresh_hub_scores(self.is_flipped)

    def setup_revamp_connections(self):
        """Pure Routing: Connects UI clicks to specialized Managers."""
        def handle_scoring(side, action):
            target = side if not self.is_flipped else (2 if side == 1 else 1)
            self.score_mod.actions.execute(target, action)
            self.refresh_hub_scores(self.is_flipped)

        self.ui.p1_add.clicked.connect(lambda: handle_scoring(1, "add"))
        self.ui.p2_add.clicked.connect(lambda: handle_scoring(2, "add"))
        self.ui.p1_minus.clicked.connect(lambda: handle_scoring(1, "undo"))
        self.ui.p2_minus.clicked.connect(lambda: handle_scoring(2, "undo"))
        
        # FIXED CONNECTION: Pass self.set_match_state to the manager
        self.ui.match_status_btn.clicked.connect(
            lambda: self.lifecycle_mod.start_flow(self.is_flipped, self.set_match_state)
        )
        
        self.ui.confirm_btn.clicked.connect(lambda: self.lifecycle_mod.confirm_act.execute())
        self.ui.cancel_win_btn.clicked.connect(lambda: self.lifecycle_mod.cancel_act.execute())
        self.ui.swap_btn.clicked.connect(self.handle_swap_logic)
        self.ui.apply_settings_btn.clicked.connect(self.handle_settings_logic)
        self.ui.broadcast_btn.clicked.connect(self.broadcast_mod.start_broadcast)

    def refresh_hub_scores(self, flipped_state=None):
        """Visual Refresh only. state passed from Actions."""
        state = self.is_flipped if flipped_state is None else flipped_state
        engine = self.score_mod.match_engine
        s1_val, s2_val = (engine.s1, engine.s2) if not state else (engine.s2, engine.s1)
        self.ui.s1_huge.setText(str(s1_val))
        self.ui.s2_huge.setText(str(s2_val))

    def handle_start_btn(self):
        res = self.lifecycle_mod.start_flow(self.is_flipped)
        if res == "RESET_PROMPT":
            if self.lifecycle_mod.reset_act.execute(self.is_flipped):
                self.handle_start_btn() # Restart flow after successful reset
        elif res == "STARTED":
            self.set_match_state(True)

    def handle_swap_logic(self):
        self.is_flipped = self.lifecycle_mod.swap_act.execute(self.is_flipped, self.match_started)

    def handle_settings_logic(self):
        self.settings_mod.apply_from_revamp(self.ui)
        # Re-apply names to display labels based on flip state
        self.refresh_hub_scores() 

    def set_match_state(self, started):
        """CRITICAL BRIDGE: Unlocks/Locks the Hub buttons visually."""
        self.match_started = started
        if started:
            # Sync colors to flip state
            p1_col = "#3498DB" if self.is_flipped else "#2ECC71"
            p2_col = "#2ECC71" if self.is_flipped else "#3498DB"
            self.ui.set_scoring_enabled(True, p1_col, p2_col)
        else:
            self.ui.set_scoring_enabled(False)

    def show_win_confirmation(self):
        self.match_started = False
        self.ui.set_scoring_enabled(False)
        self.score_mod.actions.match_active = False
        self.ui.flash_status("SET POINT!")
        self.ui.confirm_widget.show()