from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6.QtGui import QColor

class ScoreTab(QWidget):
    def __init__(self, engine, sync_callback, trigger_winner, trigger_standby, trigger_live):
        super().__init__()
        self.engine = engine
        self.sync_callback = sync_callback
        self.trigger_winner = trigger_winner
        self.trigger_standby = trigger_standby
        self.trigger_live = trigger_live
        
        layout = QVBoxLayout()

        # --- PUBLISH BUTTON (ORANGE) ---
        self.publish_btn = QPushButton("PUBLISH CHANGES")
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.publish_btn.clicked.connect(self.publish_all)
        layout.addWidget(self.publish_btn)

        # --- Settings ---
        h = QHBoxLayout()
        self.pts_sel = QComboBox(); self.pts_sel.addItems(["21 Points", "11 Points"])
        self.match_sel = QComboBox(); self.match_sel.addItems(["1", "3", "5"])
        h.addWidget(QLabel("Points:")); h.addWidget(self.pts_sel); h.addWidget(QLabel("Best of:")); h.addWidget(self.match_sel)
        layout.addLayout(h)

        # --- Names & Game Tracking ---
        self.p1_in = QLineEdit(self.engine.p1_name)
        self.p1_games_lbl = QLabel("Games Won: 0 / 3")
        self.p2_in = QLineEdit(self.engine.p2_name)
        self.p2_games_lbl = QLabel("Games Won: 0 / 3")
        
        layout.addWidget(QLabel("P1:")); layout.addWidget(self.p1_in); layout.addWidget(self.p1_games_lbl)
        layout.addWidget(QLabel("P2:")); layout.addWidget(self.p2_in); layout.addWidget(self.p2_games_lbl)

        # --- Score Buttons ---
        self.score_widget = QWidget()
        s_l = QHBoxLayout(self.score_widget)
        self.p1p = QPushButton("P1 +1"); self.p2p = QPushButton("P2 +1")
        self.p1p.clicked.connect(lambda: self.add_pt(1)); self.p2p.clicked.connect(lambda: self.add_pt(2))
        s_l.addWidget(self.p1p); s_l.addWidget(self.p2p)
        layout.addWidget(self.score_widget)

        # Lifecycle
        self.start_btn = QPushButton("START MATCH"); self.start_btn.clicked.connect(self.trigger_live)
        self.prep_btn = QPushButton("PREPARE NEXT MATCH"); self.prep_btn.clicked.connect(self.trigger_standby)
        layout.addWidget(self.start_btn); layout.addWidget(self.prep_btn)

        self.setLayout(layout)
        
        # Connect listeners to highlight the Publish button
        for widget in [self.p1_in, self.p2_in, self.pts_sel, self.match_sel]:
            if hasattr(widget, 'textChanged'): widget.textChanged.connect(self.set_dirty)
            else: widget.currentIndexChanged.connect(self.set_dirty)

    def set_dirty(self):
        self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 40px; font-weight: bold;")

    def publish_all(self):
        self.engine.p1_name = self.p1_in.text()
        self.engine.p2_name = self.p2_in.text()
        self.engine.pts_limit = 11 if "11" in self.pts_sel.currentText() else 21
        self.engine.match_limit = int(self.match_sel.currentText())
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 40px;")
        self.sync_callback()

    def add_pt(self, player):
        if player == 1: self.engine.s1 += 1
        else: self.engine.s2 += 1
        self.check_limits()
        self.sync_callback()

    def check_limits(self):
        # Lock buttons if limit reached
        self.p1p.setEnabled(self.engine.s1 < self.engine.pts_limit)
        self.p2p.setEnabled(self.engine.s2 < self.engine.pts_limit)
        
        # If someone won the point limit
        if self.engine.s1 >= self.engine.pts_limit or self.engine.s2 >= self.engine.pts_limit:
            # We will reuse the confirmation logic from before here...
            pass

    def update_ui_labels(self):
        target = (self.engine.match_limit // 2) + 1
        self.p1_games_lbl.setText(f"Games Won: {self.engine.g1} / {target}")
        self.p2_games_lbl.setText(f"Games Won: {self.engine.g2} / {target}")