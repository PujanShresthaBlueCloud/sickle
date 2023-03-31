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
# VIDEO = 'Video'
# WEBCAM = 'Webcam'
# RTSP = 'RTSP'
# YOUTUBE = 'YouTube'

# SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, RTSP, YOUTUBE]
SOURCES_LIST = [IMAGE]

# images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'image_to_predict.png'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'detected.png'

# video
# VIDEO_DIR = ROOT / 'videos'
# VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
# VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
# VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
# VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'
# VIDEOS_DICT = {
#     'video_1': VIDEO_1_PATH,
#     'video_2': VIDEO_2_PATH,
#     'video_3': VIDEO_3_PATH,
#     'video_4': VIDEO_4_PATH,
# }

# model
MODEL_DIR = ROOT
DETECTION_MODEL = MODEL_DIR / 'model/last22_415.pt'
# SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'


# Detected/segmented image dirpath locator
DETECT_LOCATOR = 'detect'
SEGMENT_LOCATOR = 'segment'

#csv
CSV = MODEL_DIR / 'csv/labels_my-project-name_2023-03-16-04-56-04.csv'

# Webcam
# WEBCAM_PATH = 0