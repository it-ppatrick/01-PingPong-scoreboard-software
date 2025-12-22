from GUI_Design.audience_ui import AudienceUI

class AudienceManager:
    def __init__(self, engine):
        # 1. Initialize the UI Blueprint
        self.ui = AudienceUI()
        self.engine = engine

    def update_display(self):
        """Management: Refresh all labels with the current Engine data."""
        # Update Names
        self.ui.p1_name_lbl.setText(self.engine.p1_name)
        self.ui.p2_name_lbl.setText(self.engine.p2_name)
        
        # Update Scores
        self.ui.p1_score_lbl.setText(str(self.engine.s1))
        self.ui.p2_score_lbl.setText(str(self.engine.s2))
        
        # Update Ball/Server Indicator (Visual logic only)
        if self.engine.server == 1:
            self.ui.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #7B2CBF; border: 5px solid white;")
            self.ui.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #555;")
        else:
            self.ui.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #FFD700; border: 5px solid white;")
            self.ui.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #555;")

    def switch_to(self, index, winner_text=None):
        """Management: Changes the visible screen (Welcome, Live, or Winner)."""
        if winner_text:
            self.ui.winner_screen.setText(winner_text)
        
        self.ui.stack.setCurrentIndex(index)

    def show(self):
        """Standard window command."""
        self.ui.show()