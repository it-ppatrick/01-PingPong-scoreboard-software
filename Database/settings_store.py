class SettingsStore:
    """Manages the configuration state of the match."""
    def __init__(self, engine):
        self.engine = engine
        
        # Default Staging Values
        self.p1_name = "HOME"
        self.p2_name = "GUEST"
        self.points_limit = 21
        self.match_limit = 3
        
    def update_names(self, n1, n2):
        """Updates names in the engine."""
        self.p1_name = n1
        self.p2_name = n2
        self.engine.p1_name = n1
        self.engine.p2_name = n2

    def update_limits(self, pts, matches):
        """Updates match rules."""
        self.points_limit = pts
        self.match_limit = matches
        self.engine.pts_limit = pts
        self.engine.match_limit = matches