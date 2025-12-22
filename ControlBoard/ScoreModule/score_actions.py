class ScoreActions:
    def __init__(self, engine, sync_callback, trigger_win_confirm):
        self.engine = engine
        self.sync_callback = sync_callback
        self.trigger_win_confirm = trigger_win_confirm

    def handle_add_point(self, player):
        """Action: Adds a point and checks for a win state."""
        self.engine.add_point(player)
        
        # Check if the logic engine says someone reached the limit
        if self.engine.check_win():
            self.trigger_win_confirm()
            
        self.sync_callback()

    def handle_undo_point(self, player):
        """Action: Reverts the point and the server in one go."""
        self.engine.undo_point(player)
        self.sync_callback()

    def handle_manual_swap(self):
        """Action: Forces a ball swap without changing the score."""
        self.engine.manual_server_swap()
        self.sync_callback()