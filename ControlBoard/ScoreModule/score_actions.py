class ScoreActions:
    def __init__(self, engine, sync_callback, win_callback):
        self.engine = engine
        self.sync_callback = sync_callback
        self.win_callback = win_callback
        self.match_active = False # Initial lock

    def execute(self, player, action_type):
        """Routes the command from the Hub to logic."""
        if not self.match_active:
            return

        if action_type == "add":
            self.add_point(player)
        elif action_type == "undo":
            self.undo_point(player)

    def add_point(self, player):
        """Adds point and checks for win conditions."""
        if player == 1:
            self.engine.s1 += 1
        else:
            self.engine.s2 += 1
        
        # Update server rotation and sync both screens
        self.engine.update_server()
        self.sync_callback()
        
        # Check if someone reached the limit
        self._check_for_winner()

    def undo_point(self, player):
        """Reduces score safely."""
        if player == 1:
            self.engine.s1 = max(0, self.engine.s1 - 1)
        else:
            self.engine.s2 = max(0, self.engine.s2 - 1)
        
        self.engine.update_server()
        self.sync_callback()

    def _check_for_winner(self):
        """Enforces point limits and triggers the Win Popup."""
        limit = self.engine.pts_limit
        s1 = self.engine.s1
        s2 = self.engine.s2

        # Logical Check: Has someone reached the limit AND are they 2 points ahead?
        # (Table tennis rules: win by 2 if you hit deuce)
        if (s1 >= limit or s2 >= limit) and abs(s1 - s2) >= 2:
            self.match_active = False # Stop the game immediately
            self.win_callback()       # Signal the Hub to show the red popup