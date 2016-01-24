import PyQt4.QtGui as QtGui
import logging
import socket
import sys
import os
import platform
import psutil

# global logging setting
logging.basicConfig(level=logging.CRITICAL)

logging.info('reading settings file')

# system information
platform = platform.system()
OPERATING_SYSTEM = str(platform).lower()
ARCHITECTURES = ['x32', 'x64']
ARCHITECTURE = None
if sys.maxsize <= 2**32:
    ARCHITECTURE = ARCHITECTURES[0]
elif sys.maxsize > 2**32:
    ARCHITECTURE = ARCHITECTURES[1]

here = os.path.dirname(os.path.realpath(__file__))

PYPELYNE2_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(here)))
QSS_ENABLE = False
QSS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'qss')
QSS_FILE = os.path.join(QSS_DIR, 'dark.css')
ICONS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'icons')
ICON_X32 = os.path.join(ICONS_DIR, 'icon_x32.png')
ICON_X64 = os.path.join(ICONS_DIR, 'icon_x64.png')
ICON_AGNOSTIC = os.path.join(ICONS_DIR, 'icon_agnostic.png')
ICON_SUBMITTER = os.path.join(ICONS_DIR, 'icon_submit.png')
ICON_LOCKED = os.path.join(ICONS_DIR, 'locked.png')
ICON_MAXIMIZE = os.path.join(ICONS_DIR, 'maximize.png')
ICON_COLLAPSE = os.path.join(ICONS_DIR, 'collapse.png')
ICON_EXPAND = os.path.join(ICONS_DIR, 'expand.png')
ICON_THUMBNAIL_PLACEHOLDER = [x for x in os.listdir(os.path.join(ICONS_DIR, 'rand_img')) if not x.startswith('.')]
ICON_THUMBNAIL_DEFAULT = os.path.join(ICONS_DIR, 'no_thumbnail.png')
ICON_FORMATS = ['.jpeg', '.jpg', '.png', '.gif']
EXCLUSIONS = ['.mayaSwatches', '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini']
DEPARTMENTS = ['LRC', 'RND', 'Layout', 'Animation']
ROLES = ['Head', 'Lead', 'Senior Artist', 'Artist', 'Junior Artist', 'Trainee', 'Intern', 'Consultant']

DOCK_ANIMATED = False
DOCK_NESTING = True

# Users module
USERS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'users')
USERS_FILES = [x for x in os.listdir(USERS_DIR) if not x.startswith('_') and not os.path.isdir(x) and x.endswith('.json')]
USERS_ICONS = os.path.join(USERS_DIR, '_icons')
USERS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_user_icon.png')

# Plugin module
PLUGINS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'plugins')
PLUGINS_FILES = [x for x in os.listdir(PLUGINS_DIR) if not x.startswith('_') and not os.path.isdir(x) and x.endswith('.json')]
PLUGINS_ICONS = os.path.join(PLUGINS_DIR, '_icons')
PLUGINS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_plugin_icon.png')
PLUGINS_ICON_HEIGHT = 40
ICON_HEIGHT = 20
CAPTURE_ICON_START = os.path.join(ICONS_DIR, 'capture_start.png')
CAPTURE_ICON_STOP = os.path.join(ICONS_DIR, 'capture_stop.png')
KILL_ICON = os.path.join(ICONS_DIR, 'kill.png')
HIDE_CONSOLE = False
NODE_STATES = ['on hold', 'start', 'in progress', 'awaiting data', 'awaiting approval', 'approved', 'rejected']

# Output module
OUTPUTS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'outputs')
OUTPUTS_FILE = os.path.join(OUTPUTS_DIR, 'outputs.json')
OUTPUTS_ICONS = os.path.join(OUTPUTS_DIR, '_icons')
OUTPUTS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_output_icon.png')
OUTPUTS_ICON_HEIGHT = PLUGINS_ICON_HEIGHT

# dockwidget_plugins module
DISPLAY_ONLY_AVAILABLE = False
DISPLAY_X32 = False
DISPLAY_X64 = True

# Task module
TASKS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'tasks')
TASKS_FILE = os.path.join(TASKS_DIR, 'tasks.json')
# TASKS_FILE = [x for x in os.listdir(TASKS_DIR) if x.endswith('.json')]



# Server and Client modules
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
except Exception, e:
    print 'could not get local ip: %s' % e
    ip = '127.0.0.1'
SERVER_IP = ip
SERVER_PORT = 5678

# ScreenGrabber module
FPS = 2
CURSOR_ICON = os.path.join(ICONS_DIR, 'cursor_reddot.png')
CURSOR = True
CURSOR_SIZE = 30
PADDING = 10
SCALE_FACTOR = 0.5
GRABBER_FORMAT = 'PNG'
# min 0, max 100, default -1
GRABBER_QUALITY = -1
TEST_MODE = True
TEST_LOOP = False
TEST_TIME = 10
ENABLE_SKIP_GAPS = True
GRABBER_AUTO_START = False

# MainWindow
SPLASH = True
SPLASH_ICON = os.path.join(ICONS_DIR, 'pypelyne.png')
SHOW_PLUGINS = True
# SHOW_PLAYER = True
SHOW_OUTPUT_WINDOWS = True
TABIFY_OUTPUT_WINDOWS = True
CLOSE_DOCK_AFTER_PLUGIN_CLOSE = False
SHOW_OUTPUT_CHANNELS = True

# Resources
ENABLE_CPU = True
ENABLE_MEM = True
ENABLE_DSK = True
COLOR_LOW = QtGui.QColor(100, 255, 100)
COLOR_MID = QtGui.QColor(255, 180, 100)
COLOR_HIGH = QtGui.QColor(255, 100, 100)
COLOR_TEXT = QtGui.QColor(0, 0, 0)
THRESHOLD_MID = 0.7
THRESHOLD_HIGH = 0.9
SECTION_COUNT = 10
REFRESH_INTERVAL = 1500
SHOW_RESOURCES = True
# mem = int(float(psutil.virtual_memory().total))
TOTAL_MEM = int(float(psutil.virtual_memory().total)/1024/1024)
MEM_MULT = 1
if TOTAL_MEM > 9000:
    MEM_MULT = 1024

disks = psutil.disk_partitions(all=False)
TOTAL_DSK = int(float(psutil.disk_usage(disks[0].mountpoint).total)/1000/1000/1000)

# Player
MP3_ROOT = r'/Users/michaelmussato/Music/mp3'
AUDIO_EXTENSIONS = [ '.mp3', '.m4a', '.mp4' ]

# NodeGraphicsItem
NODE_ROUNDNESS = 5
NODE_CREATE_COLLAPSED = False
PREVIEW_ROUNDNESS = 7
ENABLE_GIF_PREVIEW = True
DISABLE_GIF_AUTOSTART = True
COLOR_LABEL = '#080808'
ZOOM_INCREMENT = 0.100
# ZOOM_MIN = 0.01
# ZOOM_MAX = 10.0

# Node
ICON_SCALE = float(0.5)
