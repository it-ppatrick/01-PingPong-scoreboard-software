from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton
from Display.ControlBoard.live_status import LiveStatusMonitor

class ScoreTab(QWidget):
    def __init__(self, engine, sync_callback, trigger_winner, trigger_standby, trigger_live):
        super().__init__()
        self.engine = engine
        self.sync_callback = sync_callback
        self.trigger_winner = trigger_winner
        self.trigger_standby = trigger_standby
        self.trigger_live = trigger_live
        
        main_layout = QVBoxLayout()

        # 1. LIVE MONITOR (V01.05-UL)
        self.monitor = LiveStatusMonitor()
        main_layout.addWidget(self.monitor)

        # 2. TOP ACTION BAR (Publish / Swap)
        top_actions = QHBoxLayout()
        self.publish_btn = QPushButton("PUBLISH CHANGES")
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 50px; font-weight: bold;")
        self.publish_btn.clicked.connect(self.publish_all)
        
        self.swap_btn = QPushButton("SWAP SIDES ⇄")
        self.swap_btn.setStyleSheet("background-color: #7B2CBF; color: white; height: 50px; font-weight: bold;")
        self.swap_btn.clicked.connect(self.handle_swap)
        
        top_actions.addWidget(self.publish_btn, 2)
        top_actions.addWidget(self.swap_btn, 1)
        main_layout.addLayout(top_actions)

        # 3. SETTINGS ROW
        settings_h = QHBoxLayout()
        self.pts_select = QComboBox(); self.pts_select.addItems(["21 Points", "11 Points"])
        self.match_select = QComboBox(); self.match_select.addItems(["1", "3", "5"])
        settings_h.addWidget(QLabel("Points:")); settings_h.addWidget(self.pts_select)
        settings_h.addWidget(QLabel("Best of:")); settings_h.addWidget(self.match_select)
        main_layout.addLayout(settings_h)

        # 4. PLAYER NAMES (Horizontal)
        names_h = QHBoxLayout()
        self.p1_in = QLineEdit(self.engine.p1_name); self.p1_in.setPlaceholderText("P1 Name")
        self.p2_in = QLineEdit(self.engine.p2_name); self.p2_in.setPlaceholderText("P2 Name")
        names_h.addWidget(self.p1_in); names_h.addWidget(self.p2_in)
        main_layout.addLayout(names_h)

        # 5. THE DUAL-DECK SCORING (BIG BUTTONS)
        self.score_widget = QWidget()
        deck_layout = QHBoxLayout(self.score_widget)
        
        # Player 1 Column
        p1_col = QVBoxLayout()
        self.p1_games_lbl = QLabel("Games: 0"); self.p1_games_lbl.setStyleSheet("font-size: 14pt; color: #7B2CBF; font-weight: bold;")
        self.p1p = QPushButton("+1")
        self.p1p.setStyleSheet("background-color: #7B2CBF; color: white; font-size: 40pt; height: 150px; border-radius: 10px;")
        self.p1m = QPushButton("-1")
        self.p1m.setStyleSheet("background-color: #333; color: #7B2CBF; font-size: 15pt; height: 40px;")
        p1_col.addWidget(self.p1_games_lbl); p1_col.addWidget(self.p1p); p1_col.addWidget(self.p1m)
        
        # Player 2 Column
        p2_col = QVBoxLayout()
        self.p2_games_lbl = QLabel("Games: 0"); self.p2_games_lbl.setStyleSheet("font-size: 14pt; color: #FFD700; font-weight: bold;")
        self.p2p = QPushButton("+1")
        self.p2p.setStyleSheet("background-color: #FFD700; color: black; font-size: 40pt; height: 150px; border-radius: 10px;")
        self.p2m = QPushButton("-1")
        self.p2m.setStyleSheet("background-color: #333; color: #FFD700; font-size: 15pt; height: 40px;")
        p2_col.addWidget(self.p2_games_lbl); p2_col.addWidget(self.p2p); p2_col.addWidget(self.p2m)

        deck_layout.addLayout(p1_col); deck_layout.addLayout(p2_col)
        self.score_widget.hide()
        main_layout.addWidget(self.score_widget)

        # 6. LIFECYCLE BUTTONS
        self.start_btn = QPushButton("START MATCH")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; height: 60px; font-size: 18pt; font-weight: bold;")
        self.prep_btn = QPushButton("PREPARE NEXT MATCH")
        self.prep_btn.setStyleSheet("background-color: #2196F3; color: white; height: 60px; font-size: 18pt; font-weight: bold;")
        self.prep_btn.hide()
        main_layout.addWidget(self.start_btn); main_layout.addWidget(self.prep_btn)

        # Win Confirm & Listeners (Same as V01.04)
        self.setup_confirm_area(main_layout)
        self.setLayout(main_layout)
        self.setup_listeners()

    def setup_confirm_area(self, layout):
        self.win_confirm_widget = QWidget(); self.win_confirm_widget.hide()
        win_l = QVBoxLayout(self.win_confirm_widget)
        self.win_label = QLabel("Confirm Win?"); self.win_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        win_btns = QHBoxLayout()
        y_btn = QPushButton("Confirm Win"); y_btn.setStyleSheet("background-color: green; color: white; height: 40px;")
        n_btn = QPushButton("Cancel Win"); n_btn.setStyleSheet("background-color: red; color: white; height: 40px;")
        y_btn.clicked.connect(self.on_confirm); n_btn.clicked.connect(self.on_cancel)
        win_btns.addWidget(y_btn); win_btns.addWidget(n_btn)
        win_l.addWidget(self.win_label); win_l.addLayout(win_btns)
        layout.addWidget(self.win_confirm_widget)

    def setup_listeners(self):
        self.p1_in.textChanged.connect(self.set_dirty)
        self.p2_in.textChanged.connect(self.set_dirty)
        self.pts_select.currentIndexChanged.connect(self.set_dirty)
        self.match_select.currentIndexChanged.connect(self.set_dirty)
        # Minus buttons
        self.p1m.clicked.connect(lambda: self.add_pt(1, minus=True))
        self.p2m.clicked.connect(lambda: self.add_pt(2, minus=True))

    def set_dirty(self):
        self.is_dirty = True
        self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 50px; font-weight: bold;")
        self.start_btn.setEnabled(False)

    def publish_all(self):
        self.is_dirty = False
        self.engine.p1_name, self.engine.p2_name = self.p1_in.text(), self.p2_in.text()
        self.engine.pts_limit = 11 if "11" in self.pts_select.currentText() else 21
        self.engine.match_limit = int(self.match_select.currentText())
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 50px; font-weight: bold;")
        self.start_btn.setEnabled(True)
        self.sync_callback()

    def handle_swap(self):
        self.p1_in.blockSignals(True); self.p2_in.blockSignals(True)
        self.engine.swap_players()
        self.p1_in.setText(self.engine.p1_name); self.p2_in.setText(self.engine.p2_name)
        self.update_game_labels()
        self.p1_in.blockSignals(False); self.p2_in.blockSignals(False)
        self.sync_callback()

    def add_pt(self, player, minus=False):
        if not hasattr(self, 'match_active') or not self.match_active: return
        val = -1 if minus else 1
        if player == 1: self.engine.s1 = max(0, self.engine.s1 + val)
        else: self.engine.s2 = max(0, self.engine.s2 + val)
        
        # Win logic check (only on +1)
        if not minus:
            limit = self.engine.pts_limit
            s1, s2 = self.engine.s1, self.engine.s2
            lead = abs(s1 - s2)
            if (s1 >= limit or s2 >= limit) and (s1 < limit-1 or s2 < limit-1 or lead >= 2):
                self.trigger_win_confirm()
        self.sync_callback()

    def trigger_win_confirm(self):
        self.match_active = False; self.score_widget.setEnabled(False)
        name = self.p1_in.text() if self.engine.s1 > self.engine.s2 else self.p2_in.text()
        self.win_label.setText(f"Confirm <b>{name}</b> won?")
        self.win_confirm_widget.show()

    def on_confirm(self):
        if self.engine.s1 > self.engine.s2: self.engine.g1 += 1
        else: self.engine.g2 += 1
        self.engine.s1, self.engine.s2 = 0, 0
        self.update_game_labels(); self.win_confirm_widget.hide()
        req_wins = (self.engine.match_limit // 2) + 1
        if self.engine.g1 >= req_wins or self.engine.g2 >= req_wins:
            self.trigger_winner(is_game_winner=True)
            self.score_widget.hide(); self.start_btn.hide(); self.prep_btn.show()
        else:
            self.trigger_winner(is_game_winner=False)
            self.score_widget.hide(); self.start_btn.setText("START DECIDING MATCH"); self.start_btn.show()
        self.sync_callback()

    def on_cancel(self):
        # Subtract the point that caused the trigger
        if self.engine.s1 > self.engine.s2: self.engine.s1 -= 1
        else: self.engine.s2 -= 1
        self.match_active = True; self.score_widget.setEnabled(True); self.win_confirm_widget.hide()
        self.sync_callback()

    def update_game_labels(self):
        self.p1_games_lbl.setText(f"Games: {self.engine.g1}")
        self.p2_games_lbl.setText(f"Games: {self.engine.g2}")

    def handle_start_match(self):
        self.match_active = True
        self.score_widget.show(); self.score_widget.setEnabled(True)
        self.start_btn.hide()
        self.trigger_live()