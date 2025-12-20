from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton

class ScoreTab(QWidget):
    def __init__(self, engine, sync_callback, trigger_winner, trigger_standby, trigger_live):
        super().__init__()
        self.engine = engine
        self.sync_callback = sync_callback
        self.trigger_winner = trigger_winner
        self.trigger_standby = trigger_standby
        self.trigger_live = trigger_live
        
        layout = QVBoxLayout()

        self.publish_btn = QPushButton("PUBLISH CHANGES")
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.publish_btn.clicked.connect(self.publish_all)
        layout.addWidget(self.publish_btn)

        h = QHBoxLayout()
        self.pts_select = QComboBox(); self.pts_select.addItems(["21 Points", "11 Points"])
        self.match_select = QComboBox(); self.match_select.addItems(["1", "3", "5"])
        h.addWidget(QLabel("Points:")); h.addWidget(self.pts_select); h.addWidget(QLabel("Best of:")); h.addWidget(self.match_select)
        layout.addLayout(h)

        self.p1_in = QLineEdit(self.engine.p1_name); self.p1_games_lbl = QLabel("Games Won: 0")
        self.p2_in = QLineEdit(self.engine.p2_name); self.p2_games_lbl = QLabel("Games Won: 0")
        layout.addWidget(QLabel("P1:")); layout.addWidget(self.p1_in); layout.addWidget(self.p1_games_lbl)
        layout.addWidget(QLabel("P2:")); layout.addWidget(self.p2_in); layout.addWidget(self.p2_games_lbl)

        self.score_widget = QWidget()
        s_l = QHBoxLayout(self.score_widget)
        self.p1p = QPushButton("P1 +1"); self.p2p = QPushButton("P2 +1")
        self.p1p.clicked.connect(lambda: self.add_pt(1)); self.p2p.clicked.connect(lambda: self.add_pt(2))
        s_l.addWidget(self.p1p); s_l.addWidget(self.p2p)
        layout.addWidget(self.score_widget)

        self.win_confirm_widget = QWidget(); self.win_confirm_widget.hide()
        win_l = QVBoxLayout(self.win_confirm_widget)
        self.win_label = QLabel("Confirm Win?")
        win_btns = QHBoxLayout()
        y_btn = QPushButton("Confirm Win"); y_btn.clicked.connect(self.on_confirm)
        n_btn = QPushButton("Cancel"); n_btn.clicked.connect(self.win_confirm_widget.hide)
        win_btns.addWidget(y_btn); win_btns.addWidget(n_btn)
        win_l.addWidget(self.win_label); win_l.addLayout(win_btns)
        layout.addWidget(self.win_confirm_widget)

        self.start_btn = QPushButton("START MATCH"); self.start_btn.clicked.connect(self.trigger_live)
        self.prep_btn = QPushButton("PREPARE NEXT MATCH"); self.prep_btn.clicked.connect(self.trigger_standby)
        self.prep_btn.hide()
        layout.addWidget(self.start_btn); layout.addWidget(self.prep_btn)

        self.setLayout(layout)
        
        for widget in [self.p1_in, self.p2_in, self.pts_select, self.match_select]:
            if isinstance(widget, QLineEdit): widget.textChanged.connect(self.set_dirty)
            else: widget.currentIndexChanged.connect(self.set_dirty)

    def set_dirty(self):
        self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 40px; font-weight: bold;")

    def publish_all(self):
        self.engine.p1_name, self.engine.p2_name = self.p1_in.text(), self.p2_in.text()
        self.engine.pts_limit = 11 if "11" in self.pts_select.currentText() else 21
        self.engine.match_limit = int(self.match_select.currentText())
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.sync_callback()

    def add_pt(self, player):
        if player == 1: self.engine.s1 += 1
        else: self.engine.s2 += 1
        limit = self.engine.pts_limit
        if self.engine.s1 >= limit or self.engine.s2 >= limit:
            self.p1p.setEnabled(False); self.p2p.setEnabled(False)
            name = self.p1_in.text() if self.engine.s1 > self.engine.s2 else self.p2_in.text()
            self.win_label.setText(f"Confirm <b>{name}</b> won this match?")
            self.win_confirm_widget.show()
        self.sync_callback()

    def on_confirm(self):
        if self.engine.s1 > self.engine.s2: self.engine.g1 += 1
        else: self.engine.g2 += 1
        self.engine.s1, self.engine.s2 = 0, 0
        self.p1p.setEnabled(True); self.p2p.setEnabled(True)
        self.win_confirm_widget.hide()
        self.update_game_labels()
        
        req_wins = (self.engine.match_limit // 2) + 1
        if self.engine.g1 >= req_wins or self.engine.g2 >= req_wins:
            self.trigger_winner(is_game_winner=True)
            self.score_widget.hide()
            self.start_btn.hide()
            self.prep_btn.setText("PREPARE NEXT MATCH")
            self.prep_btn.show()
        else:
            self.trigger_winner(is_game_winner=False)
            # V01.03-IL: Handle the tie-breaker/deciding match button
            self.score_widget.hide()
            self.start_btn.setText("START DECIDING MATCH")
            self.start_btn.setStyleSheet("background-color: #FFD700; color: black; font-weight: bold; height: 40px;")
            self.start_btn.show()
        self.sync_callback()

    def update_game_labels(self):
        self.p1_games_lbl.setText(f"Games Won: {self.engine.g1}")
        self.p2_games_lbl.setText(f"Games Won: {self.engine.g2}")