from pathlib import Path
import sys

# add base project path to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

__version__ = "0.1.0"
