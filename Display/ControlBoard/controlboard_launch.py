from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from Database.match_logic import MatchEngine
from Display.ControlBoard.score_tab import ScoreTab
from Display.ControlBoard.displays_tab import DisplaysTab

class ControlBoard(QMainWindow):
    def __init__(self, public_display):
        super().__init__()
        self.display = public_display
        self.engine = MatchEngine()
        self.setWindowTitle("Pro-Deck Controller")
        self.setFixedSize(500, 750)

        self.score_tab = ScoreTab(self.engine, self.sync, self.trigger_winner, self.trigger_standby, self.trigger_live, self.display)
        self.displays_tab = DisplaysTab(self.display)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.score_tab, "Live Deck")
        self.tabs.addTab(self.displays_tab, "Screen Config")
        self.setCentralWidget(self.tabs); self.sync()

    def trigger_live(self):
        self.display.set_view(0)
        self.score_tab.monitor.update_status("LIVE: SCOREBOARD", "#4CAF50")
        self.sync()

    def trigger_winner(self, is_game_winner=False):
        winner = self.score_tab.p1_in.text() if self.engine.s1 > self.engine.s2 or self.engine.g1 > self.engine.g2 else self.score_tab.p2_in.text()
        self.display.show_winner(winner, is_game_winner)
        self.score_tab.monitor.update_status("DISPLAYING: WINNER", "#FFD700")

    def trigger_standby(self):
        self.engine.reset()
        self.score_tab.match_active = False
        self.score_tab.pts_select.setEnabled(True); self.score_tab.match_select.setEnabled(True) # Unlock
        self.score_tab.score_widget.hide(); self.score_tab.p1_in.clear(); self.score_tab.p2_in.clear()
        self.score_tab.update_game_labels(); self.display.set_view(2)
        self.score_tab.monitor.update_status("STATE: STANDBY", "#2196F3")
        self.score_tab.prep_btn.hide(); self.score_tab.start_btn.setText("START MATCH"); self.score_tab.start_btn.show(); self.sync()

    def sync(self):
        self.display.update_match(self.engine.p1_name, self.engine.p2_name, self.engine.s1, self.engine.s2, self.engine.g1, self.engine.g2, self.engine.match_limit, self.engine.server)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Close the controller?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes: self.display.close(); event.accept()
        else: event.ignore()