from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
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
        self.score_tab = ScoreTab(self.engine, self.sync, self.trigger_winner, self.trigger_standby, self.trigger_live)
        self.displays_tab = DisplaysTab(self.display)
        
        self.tabs.addTab(self.score_tab, "Controls")
        self.tabs.addTab(self.displays_tab, "Screen")
        self.setCentralWidget(self.tabs)
        self.sync()

    # V01.03-IL: Exit Confirmation
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 
            "Are you sure you want to close the controller?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.display.close() # Close the audience screen too
            event.accept()
        else:
            event.ignore()

    def trigger_live(self):
        self.display.set_view(0)
        self.score_tab.score_widget.show()
        self.score_tab.start_btn.hide()
        self.score_tab.prep_btn.hide()
        self.sync()

    def trigger_winner(self, is_game_winner=False):
        winner = self.score_tab.p1_in.text() if self.engine.s1 > self.engine.s2 or self.engine.g1 > self.engine.g2 else self.score_tab.p2_in.text()
        self.display.show_winner(winner, is_game_winner)

    def trigger_standby(self):
        self.engine.reset()
        self.score_tab.p1_in.clear()
        self.score_tab.p2_in.clear()
        self.score_tab.update_game_labels()
        self.display.set_view(2)
        self.score_tab.prep_btn.hide()
        self.score_tab.start_btn.show()
        self.score_tab.score_widget.hide()
        self.sync()

    def sync(self):
        self.display.update_match(
            self.engine.p1_name, self.engine.p2_name,
            self.engine.s1, self.engine.s2, self.engine.g1, self.engine.g2,
            self.engine.match_limit, self.engine.server
        )