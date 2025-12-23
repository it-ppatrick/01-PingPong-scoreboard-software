from Database.serve_logic import ServeManager

class MatchEngine:
    def __init__(self):
        # Point Scores (Sets)
        self.s1, self.s2 = 0, 0
        # Game Scores (Match)
        self.g1, self.g2 = 0, 0
        
        self.p1_name = "PLAYER 1"
        self.p2_name = "PLAYER 2"
        
        # Match Configuration
        self.pts_limit = 21        # Points needed to win a set
        self.match_limit = 3       # "Best of" (1, 3, 5)
        self.points_per_side = 5   # Serve rotation
        
        self.starting_server = 1 
        self.server = 1

    def get_games_needed(self):
        """Calculates how many games are needed to win the match."""
        # e.g., Best of 3 returns 2. Best of 5 returns 3.
        return (self.match_limit // 2) + 1

    def check_match_winner(self):
        """Returns 1 or 2 if a player has won the match, else None."""
        needed = self.get_games_needed()
        if self.g1 >= needed: return 1
        if self.g2 >= needed: return 2
        return None

    def add_point(self, player):
        if player == 1: self.s1 += 1
        else: self.s2 += 1
        self.update_server()

    def undo_point(self, player):
        if player == 1: self.s1 = max(0, self.s1 - 1)
        else: self.s2 = max(0, self.s2 - 1)
        self.update_server()

    def update_server(self):
        calculated = ServeManager.calculate_server(self.s1, self.s2, self.points_per_side)
        if self.starting_server == 1:
            self.server = calculated
        else:
            self.server = 1 if calculated == 2 else 2

    def reset_set(self):
        """Resets points for a new set, but keeps Game scores."""
        self.s1, self.s2 = 0, 0
        self.server = self.starting_server
        self.update_server()

    def reset_full_match(self):
        """Total reset of everything."""
        self.s1, self.s2 = 0, 0
        self.g1, self.g2 = 0, 0
        self.server = self.starting_server
        self.update_server()