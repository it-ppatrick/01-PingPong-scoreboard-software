class StartMatchAction:
    def __init__(self, ui, score_actions, trigger_live):
        """
        Management: We pass only exactly what this action needs to work.
        ui: The lifecycle buttons.
        score_actions: To unlock the scoring deck.
        trigger_live: To update the public screen.
        """
        self.ui = ui
        self.score_actions = score_actions
        self.trigger_live = trigger_live

    def execute(self):
        """The logic for moving from Staging to Live."""
        # 1. Update the UI
        self.ui.start_btn.hide()
        
        # 2. Unlock the scoring logic
        self.score_actions.match_active = True
        
        # 3. Update the audience screen
        self.trigger_live()