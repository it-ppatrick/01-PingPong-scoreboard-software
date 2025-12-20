# General.py

# Colors
BACKGROUND_DARK = "#0a0a0a"   # Near black for the public display
TEXT_PRIMARY = "#FFFFFF"      # White for names
TEXT_SECONDARY = "#888888"    # Grey for surnames
ACCENT_PURPLE = "#7B2CBF"     # The purple from your image
ACCENT_GOLD = "#FFD700"       # For the "Serving" text

# Font Settings
FONT_FAMILY = "Segoe UI"      # Standard modern Windows font
SIZE_FIRSTNAME = "80pt"
SIZE_SURNAME = "30pt"
SIZE_SCORE = "180pt"

# The "Daniel Look" Style Sheet (QSS)
PUBLIC_STYLE = f"""
    QWidget {{
        background-color: {BACKGROUND_DARK};
    }}
    #FirstNameLabel {{
        color: {TEXT_PRIMARY};
        font-size: {SIZE_FIRSTNAME};
        font-weight: bold;
        border: 4px solid {ACCENT_PURPLE};
        padding: 10px 40px;
        background-color: #151515;
    }}
    #SurnameLabel {{
        color: {TEXT_SECONDARY};
        font-size: {SIZE_SURNAME};
        text-transform: uppercase;
        letter-spacing: 5px;
    }}
    #ScoreLabel {{
        color: {TEXT_PRIMARY};
        font-size: {SIZE_SCORE};
        font-weight: bold;
    }}
"""