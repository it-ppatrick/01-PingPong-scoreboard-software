class ScoreActions:
    def __init__(self, engine, ui, sync_callback, win_callback):
        self.engine = engine
        self.ui = ui
        self.sync_callback = sync_callback
        self.win_callback = win_callback 
        self.match_active = False # Buttons are locked until "Start" is pressed

    def add_point(self, player):
        """Management: Only allows scoring if match is active."""
        if not self.match_active:
            return

        self.engine.add_point(player)
        
        # Check for Win: If engine says someone won, call the Hub's win confirmation
        # Note: Ensure your MatchEngine has a check_win() method!
        if self.engine.s1 >= self.engine.pts_limit or self.engine.s2 >= self.engine.pts_limit:
            if abs(self.engine.s1 - self.engine.s2) >= 2:
                self.win_callback() 
            
        self.sync_callback()

    def undo_point(self, player):
        """Action: Reverts the point and syncs the UI."""
        if not self.match_active:
            return
            
        self.engine.undo_point(player)
        self.sync_callback()

    def manual_swap(self):
        """Action: Forces a ball swap without changing the score."""
        self.engine.manual_server_swap()
        self.sync_callback()