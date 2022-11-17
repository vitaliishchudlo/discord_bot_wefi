import sys
from pathlib import Path

# Add path of the project into venv python path if it needs
if not str(Path().absolute().parent) in sys.path:
    sys.path.append(str(Path().absolute().parent))

from bot import start_bot

if __name__ == '__main__':
    start_bot()
