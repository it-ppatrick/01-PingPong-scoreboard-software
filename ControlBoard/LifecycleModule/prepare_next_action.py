class PrepareNextAction:
    def __init__(self, ui, engine, trigger_standby):
        self.ui = ui
        self.engine = engine
        self.trigger_standby = trigger_standby

    def execute(self):
        """Full reset of all scores and returns to Welcome screen."""
        self.engine.reset_full_match()
        self.ui.prep_btn.hide()
        self.ui.start_btn.setText("START MATCH")
        self.ui.start_btn.show()
        self.trigger_standby() # Takes public screen back to Welcome/Standby