from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton

class ScoreTab(QWidget):
    def __init__(self, engine, sync_callback, trigger_winner, trigger_standby, trigger_live):
        super().__init__()
        self.engine = engine
        self.sync_callback = sync_callback
        self.trigger_winner = trigger_winner
        self.trigger_standby = trigger_standby
        self.trigger_live = trigger_live
        
        self.is_dirty = False
        self.match_active = False 
        
        layout = QVBoxLayout()

        # Publish & Swap
        self.publish_btn = QPushButton("PUBLISH CHANGES")
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.publish_btn.clicked.connect(self.publish_all)
        layout.addWidget(self.publish_btn)

        self.swap_btn = QPushButton("SWAP SIDES ⇄")
        self.swap_btn.setStyleSheet("background-color: #7B2CBF; color: white; font-weight: bold;")
        self.swap_btn.clicked.connect(self.handle_swap)
        layout.addWidget(self.swap_btn)

        # Settings
        h = QHBoxLayout()
        self.pts_select = QComboBox(); self.pts_select.addItems(["21 Points", "11 Points"])
        self.match_select = QComboBox(); self.match_select.addItems(["1", "3", "5"])
        h.addWidget(QLabel("Points:")); h.addWidget(self.pts_select); h.addWidget(QLabel("Best of:")); h.addWidget(self.match_select)
        layout.addLayout(h)

        self.p1_in = QLineEdit(self.engine.p1_name); self.p1_games_lbl = QLabel("Games Won: 0")
        self.p2_in = QLineEdit(self.engine.p2_name); self.p2_games_lbl = QLabel("Games Won: 0")
        layout.addWidget(QLabel("P1:")); layout.addWidget(self.p1_in); layout.addWidget(self.p1_games_lbl)
        layout.addWidget(QLabel("P2:")); layout.addWidget(self.p2_in); layout.addWidget(self.p2_games_lbl)

        # Score Buttons
        self.score_widget = QWidget()
        s_l = QHBoxLayout(self.score_widget)
        self.p1p = QPushButton("P1 +1"); self.p2p = QPushButton("P2 +1")
        self.p1p.clicked.connect(lambda: self.add_pt(1)); self.p2p.clicked.connect(lambda: self.add_pt(2))
        s_l.addWidget(self.p1p); s_l.addWidget(self.p2p)
        self.score_widget.hide() # Hidden until Start Match
        layout.addWidget(self.score_widget)

        # Win Confirmation
        self.win_confirm_widget = QWidget(); self.win_confirm_widget.hide()
        win_l = QVBoxLayout(self.win_confirm_widget)
        self.win_label = QLabel("Confirm Win?")
        win_btns = QHBoxLayout()
        y_btn = QPushButton("Confirm Win"); y_btn.clicked.connect(self.on_confirm)
        n_btn = QPushButton("Cancel Win"); n_btn.clicked.connect(self.on_cancel)
        win_btns.addWidget(y_btn); win_btns.addWidget(n_btn)
        win_l.addWidget(self.win_label); win_l.addLayout(win_btns)
        layout.addWidget(self.win_confirm_widget)

        self.start_btn = QPushButton("START MATCH"); self.start_btn.clicked.connect(self.handle_start_match)
        self.prep_btn = QPushButton("PREPARE NEXT MATCH"); self.prep_btn.clicked.connect(self.trigger_standby)
        self.prep_btn.hide()
        layout.addWidget(self.start_btn); layout.addWidget(self.prep_btn)

        self.setLayout(layout)
        self.last_point_by = None 
        
        # Connect Listeners
        self.p1_in.textChanged.connect(self.set_dirty)
        self.p2_in.textChanged.connect(self.set_dirty)
        self.pts_select.currentIndexChanged.connect(self.set_dirty)
        self.match_select.currentIndexChanged.connect(self.set_dirty)

    def handle_start_match(self):
        self.match_active = True
        self.score_widget.show() # FORCE SHOW
        self.score_widget.setEnabled(True)
        self.start_btn.hide()
        self.trigger_live()

    def set_dirty(self):
        if not self.is_dirty:
            self.is_dirty = True
            self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 40px; font-weight: bold;")
            self.start_btn.setEnabled(False) 

    def publish_all(self):
        self.is_dirty = False
        self.engine.p1_name, self.engine.p2_name = self.p1_in.text(), self.p2_in.text()
        self.engine.pts_limit = 11 if "11" in self.pts_select.currentText() else 21
        self.engine.match_limit = int(self.match_select.currentText())
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.start_btn.setEnabled(True)
        self.sync_callback()

    def handle_swap(self):
        # 1. Block the "Dirty" listener temporarily
        self.p1_in.blockSignals(True)
        self.p2_in.blockSignals(True)
        
        # 2. Swap data
        self.engine.swap_players()
        
        # 3. Update UI
        self.p1_in.setText(self.engine.p1_name)
        self.p2_in.setText(self.engine.p2_name)
        self.update_game_labels()
        
        # 4. Unblock listeners
        self.p1_in.blockSignals(False)
        self.p2_in.blockSignals(False)
        
        self.sync_callback()

    def add_pt(self, player):
        if not self.match_active: return
        self.last_point_by = player
        if player == 1: self.engine.s1 += 1
        else: self.engine.s2 += 1
        
        limit = self.engine.pts_limit
        s1, s2 = self.engine.s1, self.engine.s2
        is_overtime = s1 >= limit-1 and s2 >= limit-1
        lead = abs(s1 - s2)

        if (not is_overtime and (s1 >= limit or s2 >= limit)) or (is_overtime and lead >= 2):
            self.match_active = False
            self.score_widget.setEnabled(False)
            name = self.p1_in.text() if s1 > s2 else self.p2_in.text()
            self.win_label.setText(f"Confirm <b>{name}</b> won?")
            self.win_confirm_widget.show()
        
        self.sync_callback()

    def on_cancel(self):
        if self.last_point_by == 1: self.engine.s1 -= 1
        else: self.engine.s2 -= 1
        self.match_active = True
        self.score_widget.setEnabled(True)
        self.win_confirm_widget.hide()
        self.sync_callback()

    def on_confirm(self):
        if self.engine.s1 > self.engine.s2: self.engine.g1 += 1
        else: self.engine.g2 += 1
        self.engine.s1, self.engine.s2 = 0, 0
        self.update_game_labels()
        self.win_confirm_widget.hide()
        
        req_wins = (self.engine.match_limit // 2) + 1
        if self.engine.g1 >= req_wins or self.engine.g2 >= req_wins:
            self.trigger_winner(is_game_winner=True)
            self.score_widget.hide(); self.start_btn.hide(); self.prep_btn.show()
        else:
            self.trigger_winner(is_game_winner=False)
            self.score_widget.hide()
            self.start_btn.setText("START DECIDING MATCH")
            self.start_btn.show()
        self.sync_callback()

    def update_game_labels(self):
        self.p1_games_lbl.setText(f"Games Won: {self.engine.g1}")
        self.p2_games_lbl.setText(f"Games Won: {self.engine.g2}")