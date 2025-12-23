class StartMatchAction:
    def __init__(self, ui, score_actions, trigger_live):
        self.ui = ui
        self.score_actions = score_actions
        self.trigger_live = trigger_live

    def execute(self):
        """Unlocks the scoring engine and updates the TV screen."""
        self.score_actions.match_active = True
        self.trigger_live()