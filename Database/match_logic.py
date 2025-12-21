class MatchEngine:
    def __init__(self):
        # Live Data
        self.s1, self.s2 = 0, 0
        self.g1, self.g2 = 0, 0
        self.server = 1

        # Staged Data
        self.p1_name, self.p2_name = "DANIEL", "GUEST"
        self.pts_limit = 21
        self.match_limit = 3

    def swap_players(self):
        """Flips all data between Player 1 and Player 2."""
        self.s1, self.s2 = self.s2, self.s1
        self.g1, self.g2 = self.g2, self.g1
        self.p1_name, self.p2_name = self.p2_name, self.p1_name

    def reset(self):
        self.s1, self.s2, self.g1, self.g2 = 0, 0, 0, 0
        self.server = 1