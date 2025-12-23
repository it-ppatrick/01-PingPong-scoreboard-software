from GUI_Design.score_deck_ui import ScoreDeckUI
from ControlBoard.ScoreModule.score_actions import ScoreActions

class ScoreManager:
    def __init__(self, engine, sync_callback, win_callback):
        self.ui = ScoreDeckUI()
        self.actions = ScoreActions(engine, self.ui, sync_callback, win_callback)
        
        self.ui.p1_plus.clicked.connect(lambda: self.actions.add_point(1))
        self.ui.p2_plus.clicked.connect(lambda: self.actions.add_point(2))
        self.ui.p1_minus.clicked.connect(lambda: self.actions.undo_point(1))
        self.ui.p2_minus.clicked.connect(lambda: self.actions.undo_point(2))

    def get_widget(self):
        return self.ui