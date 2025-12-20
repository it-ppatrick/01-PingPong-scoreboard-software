from PyQt6.QtWidgets import QMainWindow, QTabWidget
from Database.match_logic import MatchEngine
from Display.ControlBoard.score_tab import ScoreTab
from Display.ControlBoard.displays_tab import DisplaysTab

class ControlBoard(QMainWindow):
    def __init__(self, public_display):
        super().__init__()
        self.display = public_display
        self.engine = MatchEngine()
        self.setWindowTitle("Scoreboard Controller")
        self.setFixedSize(500, 750)

        self.tabs = QTabWidget()
        
        # Initialize Tabs - Added 'trigger_live' callback
        self.score_tab = ScoreTab(self.engine, self.sync, self.trigger_winner, self.trigger_standby, self.trigger_live)
        self.displays_tab = DisplaysTab(self.display)
        
        self.tabs.addTab(self.score_tab, "Controls")
        self.tabs.addTab(self.displays_tab, "Screen")
        self.setCentralWidget(self.tabs)
        self.sync()

    def trigger_live(self):
        """Switches audience to Scoreboard and shows control buttons."""
        self.display.set_view(0)
        self.score_tab.score_controls.show()
        self.score_tab.start_match_btn.hide()
        self.score_tab.prep_match_btn.hide()
        self.sync()

    def trigger_winner(self):
        """Switches audience to Winner Screen."""
        winner = self.score_tab.p1_in.text() if self.engine.g1 > self.engine.g2 else self.score_tab.p2_in.text()
        self.display.show_winner(winner)

    def trigger_standby(self):
        """Switches audience to Standby and resets inputs for new match."""
        self.engine.reset()
        self.score_tab.p1_in.clear()
        self.score_tab.p2_in.clear()
        self.score_tab.p1_in.setPlaceholderText("Enter Player 1 Name")
        self.score_tab.p2_in.setPlaceholderText("Enter Player 2 Name")
        
        self.display.set_view(2) # Show Standby
        self.score_tab.prep_match_btn.hide()
        self.score_tab.start_match_btn.show()
        self.score_tab.score_controls.hide()
        self.sync()

    def sync(self):
        # Prevent crash if match_select is empty or non-integer
        try:
            target = int(self.score_tab.match_select.currentText())
        except ValueError:
            target = 3
            
        self.display.update_match(
            self.score_tab.p1_in.text() or "TBD", 
            self.score_tab.p2_in.text() or "TBD",
            self.engine.s1, self.engine.s2, self.engine.g1, self.engine.g2,
            target, self.engine.server
        )