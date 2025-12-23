from ControlBoard.LifecycleModule.start_match_action import StartMatchAction
from ControlBoard.LifecycleModule.confirm_win_action import ConfirmWinAction
from ControlBoard.LifecycleModule.cancel_win_action import CancelWinAction
from ControlBoard.LifecycleModule.swap_sides_action import SwapSidesAction
from ControlBoard.LifecycleModule.reset_match_action import ResetMatchAction

class LifecycleManager:
    def __init__(self, engine, score_actions, ui, triggers, sync_hub_callback):
        self.ui = ui
        # Specialized Actions
        # --- Inside LifecycleManager.__init__ ---
        self.start_act = StartMatchAction(ui, score_actions, triggers['live'])
        self.confirm_act = ConfirmWinAction(ui, engine, triggers, lambda: sync_hub_callback(None))
        self.cancel_act = CancelWinAction(ui, engine, score_actions, triggers, lambda: sync_hub_callback(None))
        self.swap_act = SwapSidesAction(ui, triggers, sync_hub_callback)
        self.reset_act = ResetMatchAction(ui, engine, triggers, sync_hub_callback)

    def start_flow(self, is_flipped, hub_callback):
        """Item 2 & 3: Decides if we start, reset, or stay locked."""
        if self.ui.confirm_widget.isVisible(): 
            self.ui.flash_status("FINISH SET BEFORE STARTING")
            return "LOCKED"
            
        if self.ui.match_status_btn.text() == "START NEW MATCH": 
            if self.reset_act.execute(is_flipped):
                self.start_act.execute()
                hub_callback(True) # UNLOCK HUB BUTTONS
                return "STARTED"
            return "RESET_CANCELLED"

        # Standard Start
        self.start_act.execute()
        hub_callback(True) # UNLOCK HUB BUTTONS
        return "STARTED"