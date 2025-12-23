import sys
import os
from PyQt6.QtWidgets import QApplication

# --- THE PATH FIX ---
# This ensures Python sees your "Database", "ControlBoard", etc. folders
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# --- THE IMPORTS ---
try:
    from Database.match_logic import MatchEngine
    from Database.settings_store import SettingsStore
    from ControlBoard.main_hub import MainControlBoard
    from AudienceView.manager import AudienceManager
except ImportError as e:
    print(f"Critical Import Error: {e}")
    print("Check if your folder names match the code exactly (e.g., Database vs database).")
    sys.exit(1)

def main():
    # Fix 1: QApplication is now properly defined and initialized here
    app = QApplication(sys.argv)

    # 1. Initialize the Brain
    engine = MatchEngine()
    settings = SettingsStore(engine)

    # 2. Initialize the Audience View
    audience = AudienceManager(engine)

    # 3. Define the Triggers (The Glue)
    triggers = {
        'sync': audience.update_display,
        'live': lambda: audience.switch_to(1),
        'standby': lambda: audience.switch_to(0),
        'winner': lambda is_game_winner: audience.switch_to(
            2, 
            winner_text=f"CHAMPION: {engine.p1_name if engine.g1 > engine.g2 else engine.p2_name}" 
            if is_game_winner else f"SET WINNER"
        )
    }

    # 4. Launch the Control Board
    control_board = MainControlBoard(engine, settings, triggers)
    
    control_board.show()
    audience.show()
    
    # Final sync to show initial names
    audience.update_display()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()