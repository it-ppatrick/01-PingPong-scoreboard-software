class CancelWinAction:
    def __init__(self, ui, engine, score_actions, sync_callback):
        self.ui = ui
        self.engine = engine
        self.score_actions = score_actions
        self.sync_callback = sync_callback

    def execute(self):
        """Rolls back the last point and re-enables match play."""
        # Roll back P1 if they were leading, otherwise P2
        winner = 1 if self.engine.s1 > self.engine.s2 else 2
        self.engine.undo_point(winner)
        
        # Re-activate UI
        self.ui.confirm_widget.hide()
        self.score_actions.match_active = True
        self.sync_callback()