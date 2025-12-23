from ControlBoard.LifecycleModule.start_match_action import StartMatchAction
from ControlBoard.LifecycleModule.confirm_win_action import ConfirmWinAction
from ControlBoard.LifecycleModule.cancel_win_action import CancelWinAction
from ControlBoard.LifecycleModule.swap_sides_action import SwapSidesAction
from ControlBoard.LifecycleModule.reset_match_action import ResetMatchAction

class LifecycleManager:
    def __init__(self, engine, score_actions, ui, triggers, sync_hub_callback):
        self.ui = ui
        self.start_act = StartMatchAction(ui, score_actions, triggers['live'])
        self.confirm_act = ConfirmWinAction(ui, engine, triggers, lambda: sync_hub_callback(None))
        self.cancel_act = CancelWinAction(ui, engine, score_actions, triggers, lambda: sync_hub_callback(None))
        self.swap_act = SwapSidesAction(ui, triggers, sync_hub_callback)
        self.reset_act = ResetMatchAction(ui, engine, triggers, sync_hub_callback)

    def start_flow(self, is_flipped):
        if self.ui.confirm_widget.isVisible(): return "LOCKED"
        if self.ui.match_status_btn.text() == "START NEW MATCH": return "RESET_PROMPT"
        self.start_act.execute()
        return "STARTED"