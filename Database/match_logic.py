class MatchEngine:
    def __init__(self):
        # Live Data (Syncs Instantly)
        self.s1, self.s2 = 0, 0
        self.g1, self.g2 = 0, 0
        self.server = 1

        # Staged Data (Needs Approval)
        self.p1_name, self.p2_name = "DANIEL", "GUEST"
        self.pts_limit = 21
        self.match_limit = 3

    def reset(self):
        self.s1, self.s2, self.g1, self.g2 = 0, 0, 0, 0
        self.server = 1