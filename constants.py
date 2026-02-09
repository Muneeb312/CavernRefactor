
WIDTH = 800
HEIGHT = 480
TITLE = "Cavern"

NUM_ROWS = 18
NUM_COLUMNS = 28

LEVEL_X_OFFSET = 50
GRID_BLOCK_SIZE = 25

ANCHOR_CENTRE = ("center", "center")
ANCHOR_CENTRE_BOTTOM = ("center", "bottom")

# Widths of the letters A to Z in the font images
CHAR_WIDTH = [27, 26, 25, 26, 25, 25, 26, 25, 12, 26, 26, 25, 33, 25, 26,
              25, 27, 26, 26, 25, 26, 26, 38, 25, 25, 25]

IMAGE_WIDTH = {"life": 44, "plus": 40, "health": 40}

LEVELS = [
    ["XXXXX     XXXXXXXX     XXXXX",
     "","","","",
     "   XXXXXXX        XXXXXXX   ",
     "","","",
     "   XXXXXXXXXXXXXXXXXXXXXX   ",
     "","","",
     "XXXXXXXXX          XXXXXXXXX",
     "","",""],
    # ... (Copy the rest of the levels from original file) ...
]

# Helper for text width
def char_width(char):
    index = max(0, ord(char) - 65)
    return CHAR_WIDTH[index]