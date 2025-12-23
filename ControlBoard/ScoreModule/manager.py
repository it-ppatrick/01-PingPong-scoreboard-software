from ControlBoard.ScoreModule.score_actions import ScoreActions

class ScoreManager:
    def __init__(self, engine, sync_callback, win_callback):
        """
        Manages the Scoring Module.
        Note: We no longer pass self.ui to ScoreActions because the Hub 
        now handles the UI-to-Logic connection.
        """
        self.match_engine = engine
        
        # FIXED: Removed 'self.ui' from the arguments
        self.actions = ScoreActions(engine, sync_callback, win_callback)

    def get_widget(self):
        """
        Legacy support: In the revamp, the Hub owns the UI, 
        so this returns None or a placeholder.
        """
        return None