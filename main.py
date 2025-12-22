import sys
from PyQt6.QtWidgets import QApplication

# 1. Import the Brain
from Database.match_logic import MatchEngine
from Database.settings_store import SettingsStore

# 2. Import the Hubs
from ControlBoard.main_hub import MainControlBoard
from AudienceView.manager import AudienceManager

def main():
    app = QApplication(sys.argv)

    # --- INITIALIZATION ---
    # Create the single source of truth (The Brain)
    engine = MatchEngine()
    settings = SettingsStore(engine)

    # Create the Audience View (The Listener)
    audience = AudienceManager(engine)

    # --- THE TRIGGER DICTIONARY ---
    # This is the "Glue" that links the two windows
    triggers = {
        'sync': audience.update_display,
        'live': lambda: audience.switch_to(1),
        'standby': lambda: audience.switch_to(0),
        'winner': lambda is_game_winner: audience.switch_to(
            2, 
            winner_text=f"CHAMPION: {engine.p1_name if engine.g1 > engine.g2 else engine.p2_name}" 
            if is_game_winner else f"SET WINNER: {engine.p1_name if engine.s1 > engine.s2 else engine.s2}"
        )
    }

    # --- STARTUP ---
    # Launch the Control Board with the Triggers
    control_board = MainControlBoard(engine, settings, triggers)
    
    # Show both windows
    control_board.show()
    audience.show()
    
    # Initial sync to set names and colors
    audience.update_display()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()