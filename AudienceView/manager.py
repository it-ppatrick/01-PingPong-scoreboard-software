from GUI_Design.audience_ui import AudienceUI

class AudienceManager:
    def __init__(self, engine):
        # 1. Initialize the UI Blueprint
        self.ui = AudienceUI()
        self.engine = engine

    def update_display(self):
        """Management: Refresh labels via the modular Score Page."""
        page = self.ui.score_page
        
        page.p1_name_lbl.setText(self.engine.p1_name)
        page.p2_name_lbl.setText(self.engine.p2_name)
        page.p1_score_lbl.setText(str(self.engine.s1))
        page.p2_score_lbl.setText(str(self.engine.s2))
        page.p1_games_lbl.setText(f"GAMES: {self.engine.g1}")
        page.p2_games_lbl.setText(f"GAMES: {self.engine.g2}")
        
        # Server Highlighting logic
        if self.engine.server == 1:
            page.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #7B2CBF; border: 5px solid white; border-radius: 15px;")
            page.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #333;")
        else:
            page.p2_score_lbl.setStyleSheet("font-size: 120pt; color: #FFD700; border: 5px solid white; border-radius: 15px;")
            page.p1_score_lbl.setStyleSheet("font-size: 120pt; color: #333;")
    
    def switch_to(self, index, winner_text=None):
        """Management: Changes the visible screen (Welcome, Live, or Winner)."""
        if winner_text:
            # CHANGE 'winner_screen' TO 'winner_page'
            self.ui.winner_page.setText(winner_text)
        
        self.ui.stack.setCurrentIndex(index)
    
    def show(self):
        """Standard window command."""
        self.ui.show()
    
    def swap_sides(self, is_flipped):
        self.ui.set_visual_flip(is_flipped)
    
    def switch_to_hype(self, match_text, detail_text):
        """Updates the modular Hype Screen and switches the stack."""
        self.ui.hype_page.players_label.setText(match_text)
        self.ui.hype_page.details_label.setText(detail_text)
        self.ui.stack.setCurrentIndex(3)