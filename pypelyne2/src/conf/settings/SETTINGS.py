import logging
import socket
import sys
import os
import platform
import psutil
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import sip as sip


here = os.path.dirname(os.path.realpath(__file__))

# global logging setting
logging.basicConfig(level=logging.INFO)

logging.info('reading settings file')

# system information
platform_os = platform.system()
OPERATING_SYSTEM = str(platform_os).lower()
ARCHITECTURES = ['x32', 'x64']
ARCHITECTURE = None
if sys.maxsize <= 2**32:
    ARCHITECTURE = ARCHITECTURES[0]
elif sys.maxsize > 2**32:
    ARCHITECTURE = ARCHITECTURES[1]

VERSION_PYTHON = platform.python_version()
VERSION_QT = QtCore.QT_VERSION_STR
VERSION_PYQT = QtCore.PYQT_VERSION_STR
VERSION_SIP = sip.SIP_VERSION_STR

SORT_PLUGINS = 'family'
SORT_PLUGINS_REVERSE = False
SORT_OUTPUTS = 'output'
SORT_OUTPUTS_REVERSE = False
SORT_TASKS = 'task'
SORT_TASKS_REVERSE = False
SORT_USERS = 'name_login'
SORT_USERS_REVERSE = False
SORT_DEPARTMENTS = 'department'
SORT_DEPARTMENTS_REVERSE = False
SORT_ROLES = 'role'
SORT_ROLES_REVERSE = False
SORT_CONTAINERS = 'type'
SORT_CONTAINERS_REVERSE = False

SORT_NODE_PORTS_PRIMARY = 'output_object.output'
# SORT_NODE_PORTS_SECONDARY = 'node_object.object_id'
SORT_NODE_PORTS_REVERSE = False
# SORT_NODE_PORTS_USE_SECONDARY = True

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
ICON_MINIMIZE = os.path.join(ICONS_DIR, 'minimize.png')
ICON_COLLAPSE = os.path.join(ICONS_DIR, 'collapse.png')
ICON_EXPAND = os.path.join(ICONS_DIR, 'expand.png')

ICON_THUMBNAIL_PLACEHOLDER = [x for x in os.listdir(os.path.join(ICONS_DIR, 'rand_img')) if not x.startswith('.')]
ICON_THUMBNAIL_DEFAULT = os.path.join(ICONS_DIR, 'no_thumbnail.png')
ICON_FORMATS = ['.jpeg', '.jpg', '.png', '.gif']
EXCLUSIONS = ['.mayaSwatches', '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini']
DEPARTMENTS = [{'id': '05febf4a-8586-499f-93b7-8af37c2fccdd', 'department': 'Concept'},
               {'id': 'a5b4cfd1-6aca-4e08-bf79-6a49738d1846', 'department': 'Modelling'},
               {'id': '4965874d-10aa-4b8a-a50c-611ab4c0689d', 'department': 'Texturing'},
               {'id': '1a8e743f-3e7e-4c82-8049-dac02fa51962', 'department': 'Layout'},
               {'id': '09da04d1-5ebe-4634-ac5f-cae344a82790', 'department': 'Animation'},
               {'id': '2ed6e13d-a2fd-422f-9e45-9c2f012fba0e', 'department': 'Lighting'},
               {'id': 'f7512556-0b5a-421e-af41-8799831bc720', 'department': 'Rendering'},
               {'id': 'c256b482-2fc6-4b57-b89e-56206880cd97', 'department': 'Effects'}]

ROLES = [{'id': '4a2a13fa-30c2-4498-8e8d-902fc3ef363f', 'role': 'Head'},
         {'id': '4c86f3c5-ff3f-4499-9435-725b8216449c', 'role': 'Lead'},
         {'id': 'e1c33945-2fa6-4b18-b39b-b29c26301c03', 'role': 'Senior Artist'},
         {'id': '99cb0fad-cb01-40cc-ab4e-960a90523d3e', 'role': 'Artist'},
         {'id': 'f6448cfd-497c-4b68-81f5-1d305c7df39c', 'role': 'Junior Artist'},
         {'id': '276b79eb-dbe6-45c2-82ec-3f73efcecf0f', 'role': 'Trainee'},
         {'id': '757ac2b7-fcb9-4e19-81f6-bee1729d93bd', 'role': 'Consultant'}]

DOCK_ANIMATED = False
DOCK_NESTING = True

# Users module
USERS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'users')
USERS_FILES = [x for x in os.listdir(USERS_DIR) if not x.startswith('_') and not os.path.isdir(x) and x.endswith('.json')]
USERS_ICONS = os.path.join(USERS_DIR, '_icons')
USERS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_user_icon.png')

# Roles module
ROLES_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'roles')
ROLES_FILE = os.path.join(ROLES_DIR, 'roles.json')

# Departments module
DEPARTMENTS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'departments')
DEPARTMENTS_FILE = os.path.join(DEPARTMENTS_DIR, 'departments.json')

# Container module
CONTAINERS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'containers')
CONTAINERS_FILE = os.path.join(CONTAINERS_DIR, 'containers.json')
CONTAINERS_ICONS = os.path.join(CONTAINERS_DIR, '_icons')
CONTAINERS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'icon_container.png')

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
NODE_STATES = [{'state': 'on hold', 'color': '#FF0000'},
               {'state': 'start', 'color': '#00FF00'},
               {'state': 'in progress', 'color': '#FFFF00'},
               {'state': 'awaiting data', 'color': '#AAAAFF'},
               {'state': 'awaiting approval', 'color': '#FFFF00'},
               {'state': 'approved', 'color': '#00FF00'},
               {'state': 'rejected', 'color': '#FF0000'}]

# Output module
OUTPUTS_DIR = os.path.join(PYPELYNE2_ROOT, 'src', 'conf', 'outputs')
OUTPUTS_FILE = os.path.join(OUTPUTS_DIR, 'outputs.json')
OUTPUTS_ICONS = os.path.join(OUTPUTS_DIR, '_icons')
OUTPUTS_DEFAULT_ICON = os.path.join(ICONS_DIR, 'default_output_icon.png')
OUTPUTS_ICON_HEIGHT = PLUGINS_ICON_HEIGHT

# dockwidget_plugins module
DISPLAY_ONLY_AVAILABLE = False
DISPLAY_X32 = True
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
FPS = 5
CURSOR_ICON = os.path.join(ICONS_DIR, 'cursor_reddot.png')
CURSOR = True
CURSOR_SIZE = 30
PADDING = 6
SCALE_FACTOR = 0.5
GRABBER_FORMAT = 'PNG'
# min 0, max 100, default -1
GRABBER_QUALITY = -1
TEST_MODE = False
TEST_LOOP = False
TEST_TIME = 10
ENABLE_SKIP_GAPS = True
GRABBER_AUTO_START = False

# MainWindow
SPLASH = True
SPLASH_ICON = os.path.join(ICONS_DIR, 'pypelyne.png')
SHOW_PLUGINS = True
SHOW_CONTAINERS = True
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

# # Player
# MP3_ROOT = r'/Users/michaelmussato/Music/mp3'
# AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.mp4']

# NodeUI
NODE_ROUNDNESS = 5
NODE_CREATE_COLLAPSED = True
PREVIEW_ROUNDNESS = 7
ENABLE_GIF_PREVIEW = True
DISABLE_GIF_AUTOSTART = True
COLOR_LABEL = '#080808'
ZOOM_INCREMENT = 0.200
OUTPUT_RADIUS = 16
CONTAINER_PORT_RADIUS = 22
CONTAINER_OUTPUT_MULT = 2.0
OUTPUT_SPACING = 3
OUTPUT_OFFSET = OUTPUT_RADIUS
# ZOOM_MIN = 0.01
# ZOOM_MAX = 10.0

# NodeCore
ICON_SCALE = float(0.5)
AUTO_GENERATE_RANDOM_OUTPUTS = False
AUTO_GENERATE_RANDOM_OUTPUTS_COUNT = 10
DISPLAY_OUTPUT_NAME = False
TRANSPARENT_OUTPUT_LABEL = False
LIGHTER_AMOUNT = 150
DARKER_AMOUNT = LIGHTER_AMOUNT
REMOVE_PORT_DISTANCE = 80
AUTO_GENERATE_RANDOM_INPUTS = False
AUTO_GENERATE_RANDOM_INPUTS_COUNT = 10

# Node editor
DISPLAY_TRANSFORM_ANCHOR = False
ENABLE_NAVIGATOR = True
NAVIGATOR_SCALE = 0.1
NAVIGATOR_R = 1
NAVIGATOR_G = 1
NAVIGATOR_B = 0
NAVIGATOR_ALPHA = 0.1
NAVIGATOR_MAX_SIZE = 0.2
CONTAINER_AREA = max(10, OUTPUT_RADIUS+OUTPUT_SPACING*2)
AUTO_CREATE_CONTAINER_INPUT = 2

# Connections
# options: [BEZIER, STRAIGHT, EDGED]
LINE_TYPE = 'BEZIER'
LINE_SWITCH_THRESHOLD = 80
LINE_WIDTH = 3.0
LINE_WIDTH_HOVER = 5.0
