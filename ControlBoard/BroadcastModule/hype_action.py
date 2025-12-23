class HypeAction:
    def __init__(self, ui, engine, trigger_hype):
        self.ui = ui
        self.engine = engine
        self.trigger_hype = trigger_hype

    def execute(self):
        """Prepares text and tells AudienceView to switch to the Hype Screen."""
        player_text = f"{self.engine.p1_name} vs {self.engine.p2_name}"
        rules_text = f"Best of {self.engine.match_limit} — {self.engine.pts_limit} Points"
        
        # Signal the AudienceManager via main.py triggers
        self.trigger_hype(player_text, rules_text)
        self.ui.flash_status("HYPE SCREEN ACTIVE")