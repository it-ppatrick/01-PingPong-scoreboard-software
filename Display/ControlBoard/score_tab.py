from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton
from Display.ControlBoard.live_status import LiveStatusMonitor

class ScoreTab(QWidget):
    def __init__(self, engine, sync_callback, trigger_winner, trigger_standby, trigger_live, public_display):
        super().__init__()
        self.engine = engine
        self.display = public_display
        self.sync_callback = sync_callback
        self.trigger_winner = trigger_winner
        self.trigger_standby = trigger_standby
        self.trigger_live = trigger_live
        
        self.monitor = LiveStatusMonitor()
        self.is_dirty = False
        self.match_active = False
        
        layout = QVBoxLayout()
        layout.addWidget(self.monitor)

        # Action Bar
        actions = QHBoxLayout()
        self.publish_btn = QPushButton("PUBLISH CHANGES")
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 50px; font-weight: bold;")
        self.publish_btn.clicked.connect(self.publish_all)
        self.swap_btn = QPushButton("SWAP SIDES ⇄")
        self.swap_btn.setStyleSheet("background-color: #7B2CBF; color: white; height: 50px; font-weight: bold;")
        self.swap_btn.clicked.connect(self.handle_staged_swap)
        actions.addWidget(self.publish_btn, 2); actions.addWidget(self.swap_btn, 1)
        layout.addLayout(actions)

        # Staging Settings
        settings_h = QHBoxLayout()
        self.pts_select = QComboBox(); self.pts_select.addItems(["21 Points", "11 Points"])
        self.match_select = QComboBox(); self.match_select.addItems(["1", "3", "5"])
        settings_h.addWidget(QLabel("Points:")); settings_h.addWidget(self.pts_select)
        settings_h.addWidget(QLabel("Best of:")); settings_h.addWidget(self.match_select)
        layout.addLayout(settings_h)

        # Player Inputs
        self.p1_in = QLineEdit(self.engine.p1_name); self.p2_in = QLineEdit(self.engine.p2_name)
        names_h = QHBoxLayout(); names_h.addWidget(self.p1_in); names_h.addWidget(self.p2_in)
        layout.addLayout(names_h)

        # Scoring Deck
        self.score_widget = QWidget()
        deck = QHBoxLayout(self.score_widget)
        
        # P1 Deck
        p1c = QVBoxLayout()
        self.p1_games_lbl = QLabel("Games: 0"); self.p1_games_lbl.setStyleSheet("color: #7B2CBF; font-weight: bold;")
        self.p1_ball_btn = QPushButton("🎾 SERVE"); self.p1_ball_btn.clicked.connect(lambda: self.set_server(1))
        self.p1p = QPushButton("+1"); self.p1p.setStyleSheet("background-color: #7B2CBF; color: white; font-size: 30pt; height: 100px;")
        self.p1m = QPushButton("-1"); self.p1m.setStyleSheet("background-color: #333; color: white; height: 35px;")
        p1c.addWidget(self.p1_games_lbl); p1c.addWidget(self.p1_ball_btn); p1c.addWidget(self.p1p); p1c.addWidget(self.p1m)
        
        # P2 Deck
        p2c = QVBoxLayout()
        self.p2_games_lbl = QLabel("Games: 0"); self.p2_games_lbl.setStyleSheet("color: #FFD700; font-weight: bold;")
        self.p2_ball_btn = QPushButton("🎾 SERVE"); self.p2_ball_btn.clicked.connect(lambda: self.set_server(2))
        self.p2p = QPushButton("+1"); self.p2p.setStyleSheet("background-color: #FFD700; color: black; font-size: 30pt; height: 100px;")
        self.p2m = QPushButton("-1"); self.p2m.setStyleSheet("background-color: #333; color: white; height: 35px;")
        p2c.addWidget(self.p2_games_lbl); p2c.addWidget(self.p2_ball_btn); p2c.addWidget(self.p2p); p2c.addWidget(self.p2m)
        
        deck.addLayout(p1c); deck.addLayout(p2c)
        self.score_widget.hide(); layout.addWidget(self.score_widget)

        # Lifecycle
        self.start_btn = QPushButton("START MATCH")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; height: 60px; font-weight: bold;")
        self.start_btn.clicked.connect(self.handle_start_match)
        self.prep_btn = QPushButton("PREPARE NEXT MATCH"); self.prep_btn.clicked.connect(self.trigger_standby)
        self.prep_btn.hide()
        layout.addWidget(self.start_btn); layout.addWidget(self.prep_btn)

        self.setup_confirm_area(layout)
        self.setLayout(layout)

        # Setup Listeners
        self.p1_in.textChanged.connect(self.set_dirty); self.p2_in.textChanged.connect(self.set_dirty)
        self.pts_select.currentIndexChanged.connect(self.set_dirty); self.match_select.currentIndexChanged.connect(self.set_dirty)
        self.p1p.clicked.connect(lambda: self.add_pt(1)); self.p2p.clicked.connect(lambda: self.add_pt(2))
        self.p1m.clicked.connect(lambda: self.add_pt(1, minus=True)); self.p2m.clicked.connect(lambda: self.add_pt(2, minus=True))

    def handle_start_match(self):
        # Enforce Screen Presence
        if not self.display.isVisible():
            self.monitor.update_status("ERROR: LAUNCH SCREEN CONFIG FIRST", "red")
            return
            
        self.match_active = True
        self.score_widget.show(); self.score_widget.setEnabled(True)
        self.pts_select.setEnabled(False); self.match_select.setEnabled(False) # Lock Settings
        self.start_btn.hide(); self.trigger_live()

    def add_pt(self, player, minus=False):
        if not self.match_active: return
        val = -1 if minus else 1
        if player == 1: self.engine.s1 = max(0, self.engine.s1 + val)
        else: self.engine.s2 = max(0, self.engine.s2 + val)
        
        # 5 Point serve logic with rewind safety
        if minus: self.engine.points_in_serve = max(0, self.engine.points_in_serve - 1)
        else: self.engine.points_in_serve += 1
        
        if self.engine.points_in_serve >= 5:
            self.engine.server = 1 if self.engine.server == 2 else 2
            self.engine.points_in_serve = 0

        # Win check
        limit, s1, s2 = self.engine.pts_limit, self.engine.s1, self.engine.s2
        if not minus and ((s1 >= limit or s2 >= limit) and abs(s1-s2) >= 2):
            self.trigger_win_confirm()
        self.sync_callback()

    def on_confirm(self):
        if self.engine.s1 > self.engine.s2: self.engine.g1 += 1
        else: self.engine.g2 += 1
        self.engine.s1, self.engine.s2, self.engine.points_in_serve = 0, 0, 0
        self.win_confirm_widget.hide(); self.update_game_labels()
        self.match_active = False; self.score_widget.hide()
        
        req_wins = (self.engine.match_limit // 2) + 1
        if self.engine.g1 >= req_wins or self.engine.g2 >= req_wins:
            self.trigger_winner(True); self.start_btn.hide(); self.prep_btn.show()
        else:
            self.trigger_winner(False); self.start_btn.setText("START NEXT MATCH"); self.start_btn.show()
        self.sync_callback()

    def set_dirty(self):
        if not self.is_dirty:
            self.is_dirty = True
            self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 50px; font-weight: bold;")
            self.start_btn.setEnabled(False)

    def publish_all(self):
        self.is_dirty = False
        self.engine.p1_name, self.engine.p2_name = self.p1_in.text(), self.p2_in.text()
        self.engine.pts_limit = 11 if "11" in self.pts_select.currentText() else 21
        self.engine.match_limit = int(self.match_select.currentText())
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 50px; font-weight: bold;")
        self.start_btn.setEnabled(True); self.sync_callback()

    def handle_staged_swap(self):
        n1, n2 = self.p1_in.text(), self.p2_in.text()
        self.p1_in.setText(n2); self.p2_in.setText(n1); self.set_dirty()

    def set_server(self, player):
        self.engine.server = player; self.engine.points_in_serve = 0; self.sync_callback()

    def trigger_win_confirm(self):
        self.match_active = False; self.score_widget.setEnabled(False)
        self.win_label.setText(f"Confirm Set Result?"); self.win_confirm_widget.show()

    def on_cancel(self):
        # Rewind the point that triggered the win check
        self.add_pt(1 if self.engine.s1 > self.engine.s2 else 2, minus=True)
        self.match_active = True; self.score_widget.setEnabled(True); self.win_confirm_widget.hide(); self.sync_callback()

    def setup_confirm_area(self, layout):
        self.win_confirm_widget = QWidget(); self.win_confirm_widget.hide()
        win_l = QVBoxLayout(self.win_confirm_widget)
        self.win_label = QLabel("Confirm Win?")
        win_btns = QHBoxLayout()
        y_btn = QPushButton("Confirm Win"); y_btn.setStyleSheet("background-color: green; color: white; height: 40px;")
        n_btn = QPushButton("Cancel Win"); n_btn.setStyleSheet("background-color: red; color: white; height: 40px;")
        y_btn.clicked.connect(self.on_confirm); n_btn.clicked.connect(self.on_cancel)
        win_btns.addWidget(y_btn); win_btns.addWidget(n_btn)
        win_l.addWidget(self.win_label); win_l.addLayout(win_btns); layout.addWidget(self.win_confirm_widget)

    def update_game_labels(self):
        self.p1_games_lbl.setText(f"Games: {self.engine.g1}"); self.p2_games_lbl.setText(f"Games: {self.engine.g2}")