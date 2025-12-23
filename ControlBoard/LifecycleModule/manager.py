from GUI_Design.lifecycle_ui import LifecycleUI
from ControlBoard.LifecycleModule.start_match_action import StartMatchAction
from ControlBoard.LifecycleModule.confirm_win_action import ConfirmWinAction
from ControlBoard.LifecycleModule.cancel_win_action import CancelWinAction
from ControlBoard.LifecycleModule.prepare_next_action import PrepareNextAction

class LifecycleManager:
    def __init__(self, engine, score_actions, trigger_live, trigger_standby, trigger_winner, sync_callback):
        self.ui = LifecycleUI()
        
        self.start_act = StartMatchAction(self.ui, score_actions, trigger_live)
        self.confirm_act = ConfirmWinAction(self.ui, engine, score_actions, trigger_winner, sync_callback)
        self.cancel_act = CancelWinAction(self.ui, engine, score_actions, sync_callback)
        self.prepare_act = PrepareNextAction(self.ui, engine, trigger_standby)
        
        self.ui.start_btn.clicked.connect(self.start_act.execute)
        self.ui.prep_btn.clicked.connect(self.prepare_act.execute)
        self.ui.yes_btn.clicked.connect(self.confirm_act.execute)
        self.ui.no_btn.clicked.connect(self.cancel_act.execute)

    def get_widget(self):
        return self.ui