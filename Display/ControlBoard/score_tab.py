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
        
        self.is_dirty = False
        self.match_active = False
        self.staged_p1, self.staged_p2 = self.engine.p1_name, self.engine.p2_name
        
        layout = QVBoxLayout()
        layout.addWidget(LiveStatusMonitor())

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

        # Names & Ball Selection
        names_h = QHBoxLayout()
        self.p1_in = QLineEdit(self.staged_p1); self.p2_in = QLineEdit(self.staged_p2)
        names_h.addWidget(self.p1_in); names_h.addWidget(self.p2_in)
        layout.addLayout(names_h)

        # Scoring Deck
        self.score_widget = QWidget()
        deck = QHBoxLayout(self.score_widget)
        
        # P1
        p1c = QVBoxLayout()
        self.p1_ball_btn = QPushButton("🎾 SERVE"); self.p1_ball_btn.clicked.connect(lambda: self.set_server(1))
        self.p1p = QPushButton("+1"); self.p1p.setStyleSheet("background-color: #7B2CBF; color: white; font-size: 30pt; height: 100px;")
        p1c.addWidget(self.p1_ball_btn); p1c.addWidget(self.p1p)
        
        # P2
        p2c = QVBoxLayout()
        self.p2_ball_btn = QPushButton("🎾 SERVE"); self.p2_ball_btn.clicked.connect(lambda: self.set_server(2))
        self.p2p = QPushButton("+1"); self.p2p.setStyleSheet("background-color: #FFD700; color: black; font-size: 30pt; height: 100px;")
        p2c.addWidget(self.p2_ball_btn); p2c.addWidget(self.p2p)
        
        deck.addLayout(p1c); deck.addLayout(p2c)
        self.score_widget.hide(); layout.addWidget(self.score_widget)

        # Start/Prep
        self.start_btn = QPushButton("START MATCH"); self.start_btn.clicked.connect(self.handle_start_match)
        self.prep_btn = QPushButton("PREPARE NEXT MATCH"); self.prep_btn.clicked.connect(self.trigger_standby)
        self.prep_btn.hide()
        self.start_btn.setStyleSheet("background-color: #4CAF50; height: 60px; font-weight: bold;")
        layout.addWidget(self.start_btn); layout.addWidget(self.prep_btn)

        self.setLayout(layout)
        self.p1p.clicked.connect(lambda: self.add_pt(1)); self.p2p.clicked.connect(lambda: self.add_pt(2))
        self.p1_in.textChanged.connect(self.set_dirty); self.p2_in.textChanged.connect(self.set_dirty)

    def set_dirty(self):
        self.is_dirty = True
        self.publish_btn.setStyleSheet("background-color: #FF8C00; color: white; height: 50px; font-weight: bold;")

    def publish_all(self):
        self.is_dirty = False
        self.engine.p1_name, self.engine.p2_name = self.p1_in.text(), self.p2_in.text()
        self.publish_btn.setStyleSheet("background-color: #555; color: white; height: 50px;")
        self.sync_callback()

    def handle_staged_swap(self):
        # Swap text in controller inputs and set dirty
        n1, n2 = self.p1_in.text(), self.p2_in.text()
        self.p1_in.setText(n2); self.p2_in.setText(n1)
        self.set_dirty()

    def set_server(self, player):
        self.engine.server = player
        self.sync_callback()

    def add_pt(self, player):
        if not self.match_active: return
        if player == 1: self.engine.s1 += 1
        else: self.engine.s2 += 1
        
        # Auto-switch ball every 2 points (standard) or 5 points
        total = self.engine.s1 + self.engine.s2
        if total % 2 == 0: 
            self.engine.server = 1 if self.engine.server == 2 else 2
            
        self.sync_callback()
        # [Add win-check logic here similar to previous versions]

    def handle_start_match(self):
        self.match_active = True
        self.score_widget.show(); self.start_btn.hide()
        self.trigger_live()