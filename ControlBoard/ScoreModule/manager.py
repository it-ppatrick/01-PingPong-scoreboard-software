from GUI_Design.score_deck_ui import ScoreDeckUI
from ControlBoard.ScoreModule.score_actions import ScoreActions

class ScoreManager:
    def __init__(self, engine, sync_callback, trigger_win):
        # 1. Initialize the GUI (The "Look")
        self.ui = ScoreDeckUI()
        
        # 2. Initialize the Actions (The "Brain")
        self.actions = ScoreActions(engine, sync_callback, trigger_win)
        
        # 3. Connect the "Look" to the "Brain"
        self.setup_connections()

    def setup_connections(self):
        """Management: Connecting visual buttons to logical functions."""
        # Player 1 Connections
        self.ui.p1_plus.clicked.connect(lambda: self.actions.handle_add_point(1))
        self.ui.p1_minus.clicked.connect(lambda: self.actions.handle_undo_point(1))
        
        # Player 2 Connections
        self.ui.p2_plus.clicked.connect(lambda: self.actions.handle_add_point(2))
        self.ui.p2_minus.clicked.connect(lambda: self.actions.handle_undo_point(2))

    def get_widget(self):
        """Returns the completed UI for the main tab."""
        return self.ui