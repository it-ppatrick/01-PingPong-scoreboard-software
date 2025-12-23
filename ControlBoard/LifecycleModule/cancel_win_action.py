class CancelWinAction:
    def __init__(self, ui, engine, score_actions, triggers, sync_hub_callback):
        self.ui = ui
        self.engine = engine
        self.score_actions = score_actions
        self.triggers = triggers
        self.sync_hub = sync_hub_callback

    def execute(self):
        """Reverts point directly and re-activates scoring."""
        if self.engine.s1 > self.engine.s2:
            self.engine.s1 = max(0, self.engine.s1 - 1)
        else:
            self.engine.s2 = max(0, self.engine.s2 - 1)
            
        self.score_actions.match_active = True
        self.ui.confirm_widget.hide()
        
        # Determine colors for UI re-enable
        # We'll pass the colors logic from the manager/hub
        self.sync_hub()
        self.triggers['sync']()
        self.ui.flash_status("POINT REVERTED")