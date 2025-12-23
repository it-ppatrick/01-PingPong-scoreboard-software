from GUI_Design.audience_ui import AudienceUI

class AudienceManager:
    def __init__(self, engine):
        # 1. Initialize the UI Blueprint
        self.ui = AudienceUI()
        self.engine = engine

    def update_display(self):
        """Management: Refresh all labels with the current Engine data."""
        # 1. Update Names
        self.ui.p1_name_lbl.setText(self.engine.p1_name)
        self.ui.p2_name_lbl.setText(self.engine.p2_name)
        
        # 2. Update Points (Current Set)
        self.ui.p1_score_lbl.setText(str(self.engine.s1))
        self.ui.p2_score_lbl.setText(str(self.engine.s2))
        
        # 3. Update Games/Sets (The overall match score)
        # We access g1 and g2 from your updated MatchEngine
        self.ui.p1_games_lbl.setText(f"GAMES: {self.engine.g1}")
        self.ui.p2_games_lbl.setText(f"GAMES: {self.engine.g2}")
        
        # 4. Update Ball/Server Indicator (Visual logic only)
        if self.engine.server == 1:
            # Player 1 is serving: Highlight purple, dim Player 2
            self.ui.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #7B2CBF; border: 5px solid white; border-radius: 15px;")
            self.ui.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #333;")
        else:
            # Player 2 is serving: Highlight Gold, dim Player 1
            self.ui.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #FFD700; border: 5px solid white; border-radius: 15px;")
            self.ui.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #333;")

    def switch_to(self, index, winner_text=None):
        """Management: Changes the visible screen (Welcome, Live, or Winner)."""
        if winner_text:
            self.ui.winner_screen.setText(winner_text)
        
        self.ui.stack.setCurrentIndex(index)

    def show(self):
        """Standard window command."""
        self.ui.show()