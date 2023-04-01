from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# Source
IMAGE = 'Image'

# SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, RTSP, YOUTUBE]
SOURCES_LIST = [IMAGE]

# images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'image_to_predict.png'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'detected.png'

# model
MODEL_DIR = ROOT
DETECTION_MODEL = MODEL_DIR / 'model/last22_415.pt'

# Detected/segmented image dirpath locator
DETECT_LOCATOR = 'detect'

# csv file
# CSV = MODEL_DIR / 'csv/labels_my-project-name_2023-03-16-04-56-04.csv'

# css stylesheet
CSS = MODEL_DIR/ 'css/style.css'

# javascipt file
JS = MODEL_DIR/ 'js/main.js'