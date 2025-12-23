from PyQt6.QtWidgets import QMainWindow
from GUI_Design.control_board_revamp import ControlBoardUI 
from ControlBoard.ScoreModule.manager import ScoreManager
from ControlBoard.LifecycleModule.manager import LifecycleManager
from ControlBoard.SettingsModule.manager import SettingsManager

class MainControlBoard(QMainWindow):
    def __init__(self, engine, settings_store, triggers):
        super().__init__()
        self.setWindowTitle("Table Tennis Control - V02.20")
        self.setMinimumSize(450, 650)
        self.triggers = triggers 
        
        self.ui = ControlBoardUI()
        self.setCentralWidget(self.ui)
        
        self.score_mod = ScoreManager(engine, triggers['sync'], self.show_win_confirmation)
        self.settings_mod = SettingsManager(engine, triggers['sync'])
        self.lifecycle_mod = LifecycleManager(
            engine, self.score_mod.actions, triggers['live'], 
            triggers['standby'], triggers['winner'], triggers['sync']
        )

        self.setup_revamp_connections()
        self.ui.set_scoring_enabled(False) 

    def setup_revamp_connections(self):
        # Scoring
        self.ui.p1_add.clicked.connect(lambda: self.score_mod.actions.execute(1, "add"))
        self.ui.p2_add.clicked.connect(lambda: self.score_mod.actions.execute(2, "add"))
        self.ui.p1_minus.clicked.connect(lambda: self.score_mod.actions.execute(1, "undo"))
        self.ui.p2_minus.clicked.connect(lambda: self.score_mod.actions.execute(2, "undo"))
        
        # Match/Set Control
        self.ui.match_status_btn.clicked.connect(self.begin_match_flow)
        self.ui.confirm_btn.clicked.connect(self.handle_confirm_win)
        self.ui.cancel_win_btn.clicked.connect(self.handle_cancel_win)
        self.ui.swap_btn.clicked.connect(self.handle_visual_swap)
        
        # Settings & Broadcast
        self.ui.apply_settings_btn.clicked.connect(self.handle_apply_settings)
        self.ui.broadcast_btn.clicked.connect(self.handle_broadcast)

    def begin_match_flow(self):
        self.score_mod.actions.match_active = True
        self.ui.set_scoring_enabled(True)
        self.triggers['live']() 
        self.ui.flash_status("MATCH STARTED")

    def handle_confirm_win(self):
        """Processes set results and checks if the entire match is finished."""
        engine = self.score_mod.match_engine
        
        # 1. Update Game Score
        if engine.s1 > engine.s2:
            engine.g1 += 1
        else:
            engine.g2 += 1
            
        # 2. Check Match Limit (Best of 1, 3, or 5)
        limit = 1
        if self.ui.best_3.isChecked(): limit = 2
        elif self.ui.best_5.isChecked(): limit = 3
        
        if engine.g1 >= limit or engine.g2 >= limit:
            winner_name = engine.p1_name if engine.g1 >= limit else engine.p2_name
            self.ui.flash_status(f"MATCH OVER: {winner_name} WINS!")
            self.triggers['winner']() # Final Audience Celebration
            # Keep UI locked - match is done
        else:
            engine.reset_set()
            self.triggers['sync']()
            self.ui.flash_status("SET RECORDED - READY FOR NEXT")
        
        self.ui.confirm_widget.hide()
        self.ui.set_scoring_enabled(False) 

    def handle_cancel_win(self):
        self.ui.confirm_widget.hide()
        self.ui.set_scoring_enabled(True) 
        self.score_mod.actions.match_active = True
        self.ui.flash_status("WIN CANCELLED")

    def handle_visual_swap(self):
        """Swaps labels on the Control Board without affecting the engine."""
        p1 = self.ui.p1_name_display.text()
        p2 = self.ui.p2_name_display.text()
        self.ui.p1_name_display.setText(p2)
        self.ui.p2_name_display.setText(p1)
        self.ui.flash_status("SIDES SWAPPED VISUALLY")

    def handle_apply_settings(self):
        self.settings_mod.apply_from_revamp(self.ui)
        self.ui.flash_status("SETTINGS APPLIED")
        engine_ref = getattr(self.score_mod, 'match_engine', getattr(self.score_mod, 'engine', None))
        if engine_ref:
            self.ui.p1_name_display.setText(engine_ref.p1_name)
            self.ui.p2_name_display.setText(engine_ref.p2_name)

    def handle_broadcast(self):
        self.triggers['live']() 
        self.ui.flash_status("BROADCAST LIVE")

    def show_win_confirmation(self):
        self.ui.set_scoring_enabled(False)
        self.score_mod.actions.match_active = False
        self.ui.flash_status("SET POINT!")
        self.ui.confirm_widget.show()