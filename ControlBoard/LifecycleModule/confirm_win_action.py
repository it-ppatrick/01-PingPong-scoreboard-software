class ConfirmWinAction:
    def __init__(self, ui, engine, triggers, sync_hub_callback):
        self.ui = ui
        self.engine = engine
        self.triggers = triggers
        self.sync_hub = sync_hub_callback

    def execute(self):
        """Processes results and forces engine reset on Champion."""
        if self.engine.s1 > self.engine.s2:
            self.engine.g1 += 1
        else:
            self.engine.g2 += 1
            
        limit = 2 if self.ui.best_3.isChecked() else 3 if self.ui.best_5.isChecked() else 1
        
        if self.engine.g1 >= limit or self.engine.g2 >= limit:
            winner_name = self.engine.p1_name if self.engine.g1 >= limit else self.engine.p2_name
            self.ui.flash_status(f"CHAMPION: {winner_name}!")
            self.triggers['winner'](is_game_winner=True)
            
            # Reset values immediately and lock board
            self.engine.reset_full_match() 
            self.ui.set_scoring_enabled(False, is_finished=True) 
        else:
            self.engine.reset_set()
            self.triggers['sync']()
            self.ui.flash_status("SET RECORDED")
            self.ui.set_scoring_enabled(False) 
        
        self.ui.confirm_widget.hide()
        self.sync_hub() # Refresh the Hub scores