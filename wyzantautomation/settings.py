from pathlib import Path
from models import MessageTemplate


# Root dirs
BASE_DIR = Path(__file__).parent.resolve()

IGNORE_DIR = BASE_DIR / "ignore"  # Important to not track files in these directories

# Data Storage Settings

DATA_DIR = IGNORE_DIR / "data"

SCREENSHOTS_DIR = IGNORE_DIR / "screenshots"

# Default Settings

MIN_RATE = 300  # Minimum hourly rate

# --------- Init --------- #
DATA_DIR.mkdir(exist_ok=True, parents=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True, parents=True)