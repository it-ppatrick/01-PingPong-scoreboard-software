# General.py

BACKGROUND_DARK = "#0a0a0a"   
TEXT_PRIMARY = "#FFFFFF"      
ACCENT_PURPLE = "#7B2CBF"     
ACCENT_GOLD = "#FFD700"       

PUBLIC_STYLE = f"""
    QWidget {{
        background-color: {BACKGROUND_DARK};
    }}
    #NameBox {{
        color: {TEXT_PRIMARY};
        font-size: 50pt;
        font-weight: bold;
        background-color: {ACCENT_PURPLE};
        padding: 10px 30px;
        border-radius: 5px;
    }}
    #ScoreLabel {{
        color: {TEXT_PRIMARY};
        font-size: 220pt;
        font-weight: bold;
    }}
    #GameWinLabel {{
        color: {TEXT_PRIMARY};
        font-size: 50pt;
        font-weight: bold;
    }}
"""