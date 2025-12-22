class ConfirmWinAction:
    def __init__(self, ui, engine, score_actions, trigger_winner, sync_callback):
        self.ui = ui
        self.engine = engine
        self.score_actions = score_actions
        self.trigger_winner = trigger_winner
        self.sync_callback = sync_callback

    def execute(self):
        """Processes the set result and checks for a match winner."""
        # 1. Update Game Score
        if self.engine.s1 > self.engine.s2: self.engine.g1 += 1
        else: self.engine.g2 += 1
        
        # 2. Reset points for the next set
        self.engine.reset_set()
        self.ui.confirm_widget.hide()
        
        # 3. Check if someone won the entire match (e.g., 2 sets out of 3)
        needed = (self.engine.match_limit // 2) + 1
        if self.engine.g1 >= needed or self.engine.g2 >= needed:
            self.trigger_winner(is_game_winner=True) # Full Champion Screen
            self.ui.prep_btn.show() # Offer button to clear everything for next match
        else:
            self.trigger_winner(is_game_winner=False) # Intermediate Set Winner Screen
            self.ui.start_btn.setText("START NEXT SET")
            self.ui.start_btn.show()
            
        self.sync_callback()