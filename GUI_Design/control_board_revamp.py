from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QStackedWidget, QLineEdit, QRadioButton, 
                             QListWidget, QButtonGroup, QFrame)
from PyQt6.QtCore import Qt, QTimer

class ControlBoardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Board - V02.20")
        self.setMinimumSize(450, 650)
        self.setStyleSheet("background-color: #F5F5F5;")
        
        self.main_layout = QVBoxLayout(self)
        
        # --- Navigation Tabs ---
        self.nav_layout = QHBoxLayout()
        self.btn_main = QPushButton("Main Scoring")
        self.btn_settings = QPushButton("Match Settings")
        self.btn_display = QPushButton("Display Settings")
        
        for btn in [self.btn_main, self.btn_settings, self.btn_display]:
            btn.setStyleSheet("padding: 8px; background: white; border: 1px solid #CCC;")
            self.nav_layout.addWidget(btn)
        self.main_layout.addLayout(self.nav_layout)

        # --- Stacked Screens ---
        self.stack = QStackedWidget()
        self.scoring_page = self._setup_scoring_page()
        self.settings_page = self._setup_settings_page()
        self.display_page = self._setup_display_page()
        
        self.stack.addWidget(self.scoring_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.display_page)
        self.main_layout.addWidget(self.stack)

        # --- Status Bar ---
        self.status_bar = QLabel("READY")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("background-color: #333; color: white; padding: 10px; font-weight: bold;")
        self.main_layout.addWidget(self.status_bar)

        # Tab Switching Logic
        self.btn_main.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_display.clicked.connect(lambda: self.stack.setCurrentIndex(2))

    def _setup_scoring_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Names/Swap
        header = QHBoxLayout()
        self.p1_name_display = QLabel("PLAYER 1")
        self.swap_btn = QPushButton("⇄")
        self.p2_name_display = QLabel("PLAYER 2")
        for lbl in [self.p1_name_display, self.p2_name_display]:
            lbl.setStyleSheet("font-size: 14pt; font-weight: bold;")
        header.addWidget(self.p1_name_display); header.addWidget(self.swap_btn); header.addWidget(self.p2_name_display)
        
        # Big Scores
        scores = QHBoxLayout()
        self.s1_huge = QLabel("0"); self.s2_huge = QLabel("0")
        for lbl in [self.s1_huge, self.s2_huge]:
            lbl.setStyleSheet("font-size: 80pt; font-weight: bold;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scores.addWidget(self.s1_huge); scores.addWidget(self.s2_huge)

        # Buttons
        grid = QHBoxLayout()
        p1_col = QVBoxLayout()
        self.p1_add = QPushButton("+ 1")
        self.p1_add.setStyleSheet("background-color: #2ECC71; color: white; height: 80px; font-size: 20pt; border-radius: 10px;")
        self.p1_minus = QPushButton("- 1")
        self.p1_minus.setStyleSheet("background-color: #2C3E50; color: white; height: 40px; border-radius: 5px;")
        p1_col.addWidget(self.p1_add); p1_col.addWidget(self.p1_minus)
        
        p2_col = QVBoxLayout()
        self.p2_add = QPushButton("+ 1")
        self.p2_add.setStyleSheet("background-color: #3498DB; color: white; height: 80px; font-size: 20pt; border-radius: 10px;")
        self.p2_minus = QPushButton("- 1")
        self.p2_minus.setStyleSheet("background-color: #2C3E50; color: white; height: 40px; border-radius: 5px;")
        p2_col.addWidget(self.p2_add); p2_col.addWidget(self.p2_minus)
        
        grid.addLayout(p1_col); grid.addLayout(p2_col)
        layout.addLayout(header); layout.addLayout(scores); layout.addLayout(grid)
        
        # Start Match Button
        self.match_status_btn = QPushButton("START GAME")
        self.match_status_btn.setStyleSheet("background-color: #D5D8DC; padding: 15px; font-weight: bold; border-radius: 5px;")
        layout.addWidget(self.match_status_btn)

        # --- Confirm Winner Popup UI with CANCEL option ---
        self.confirm_widget = QFrame()
        self.confirm_widget.setStyleSheet("background-color: #FDEDEC; border: 2px solid #E74C3C; border-radius: 10px; margin-top: 10px;")
        confirm_layout = QVBoxLayout(self.confirm_widget)
        
        msg = QLabel("<b>SET OVER!</b><br>Confirm the winner below:")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        confirm_layout.addWidget(msg)

        confirm_btns_layout = QHBoxLayout()
        self.cancel_win_btn = QPushButton("CANCEL")
        self.cancel_win_btn.setStyleSheet("background-color: #BDC3C7; color: #333; padding: 10px; font-weight: bold;")
        self.confirm_btn = QPushButton("CONFIRM")
        self.confirm_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 10px; font-weight: bold;")
        
        confirm_btns_layout.addWidget(self.cancel_win_btn)
        confirm_btns_layout.addWidget(self.confirm_btn)
        confirm_layout.addLayout(confirm_btns_layout)
        
        self.confirm_widget.hide() 
        layout.addWidget(self.confirm_widget)
        
        return page

    def set_scoring_enabled(self, enabled):
        """Standardizes the 'Match Active' visual state."""
        buttons = [self.p1_add, self.p1_minus, self.p2_add, self.p2_minus]
        
        for btn in buttons:
            btn.setEnabled(enabled)
            # Change opacity/color based on state
            if not enabled:
                btn.setStyleSheet(btn.styleSheet() + "background-color: #BDC3C7; color: #7F8C8D;")
            else:
                # Re-apply the original colors (you might want to store these in variables)
                if btn == self.p1_add: btn.setStyleSheet("background-color: #2ECC71; color: white; height: 80px; font-size: 20pt; border-radius: 10px;")
                elif btn == self.p2_add: btn.setStyleSheet("background-color: #3498DB; color: white; height: 80px; font-size: 20pt; border-radius: 10px;")
                else: btn.setStyleSheet("background-color: #2C3E50; color: white; height: 40px; border-radius: 5px;")

    def _setup_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>PLAYER 1 NAME</b>"))
        self.p1_input = QLineEdit(); layout.addWidget(self.p1_input)
        layout.addWidget(QLabel("<b>PLAYER 2 NAME</b>"))
        self.p2_input = QLineEdit(); layout.addWidget(self.p2_input)
        
        layout.addWidget(QLabel("<b>Points per Set</b>"))
        self.points_group = QButtonGroup(self) 
        self.pts_11 = QRadioButton("11 Points"); self.pts_21 = QRadioButton("21 Points")
        self.points_group.addButton(self.pts_11); self.points_group.addButton(self.pts_21)
        self.pts_21.setChecked(True)
        layout.addWidget(self.pts_11); layout.addWidget(self.pts_21)

        layout.addWidget(QLabel("<b>Series Length</b>"))
        self.series_group = QButtonGroup(self) 
        self.best_1 = QRadioButton("Best of 1"); self.best_3 = QRadioButton("Best of 3"); self.best_5 = QRadioButton("Best of 5")
        self.series_group.addButton(self.best_1); self.series_group.addButton(self.best_3); self.series_group.addButton(self.best_5)
        self.best_3.setChecked(True)
        layout.addWidget(self.best_1); layout.addWidget(self.best_3); layout.addWidget(self.best_5)
        
        self.apply_settings_btn = QPushButton("Apply Settings")
        self.apply_settings_btn.setStyleSheet("background-color: #F1C40F; padding: 15px; font-weight: bold;")
        layout.addWidget(self.apply_settings_btn)
        layout.addStretch()
        return page

    def _setup_display_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Available Displays</b>"))
        self.display_list = QListWidget(); self.display_list.addItem("Primary Monitor")
        layout.addWidget(self.display_list)
        
        self.broadcast_btn = QPushButton("START BROADCAST")
        self.broadcast_btn.setStyleSheet("background-color: #E67E22; color: white; padding: 20px; font-weight: bold;")
        layout.addWidget(self.broadcast_btn)
        layout.addStretch()
        return page

    def flash_status(self, message):
        self.status_bar.setText(message)
        self.status_bar.setStyleSheet("background-color: #2ECC71; color: white; padding: 10px; font-weight: bold;")
        QTimer.singleShot(5000, lambda: self.status_bar.setStyleSheet("background-color: #333; color: white; padding: 10px;"))