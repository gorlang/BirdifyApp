import configparser

class FileConfig():
    def __init__(self):
        self.BASE_PATH = "src/"
        self.cfg = configparser.RawConfigParser()
        self.cfg.read(self.BASE_PATH + 'app-config.cfg')
        self.AUDIO = dict(self.cfg.items('AUDIO'))
        self.LOGGING = dict(self.cfg.items('LOGGING'))
        self.THEME = dict(self.cfg.items('THEME'))

class AppConfig():
    def __init__(self):
        self.TEST = False
        self.VERSION = "0.5.0"
        self.APP_NAME = "Birdify!"
        self.BIRDIFY_WEB_URL = "https://knutas.com/birdify/build/"
        fc = FileConfig()
        self.THEME = fc.THEME["theme"]
        self.BASE_PATH = "src/"
        self.DEVICE_NAMES_OUT = [fc.AUDIO["output_primary"], fc.AUDIO["output_fallback"]]
        self.DEVICE_NAMES_IN = [fc.AUDIO["input"]]
        self.FONT = 'Arial'
        self.WINDOW_SIZE_SCALE = 0.5 # scaled factor to available win height
        self.AUDIO_FILE_TYPES = ["mp3", "wav"]
        self.SAMPLE_COUNT = 1024 # for audio level chart
        self.SAMPLE_RATE_HIGH = 48000
        self.SAMPLE_RATE_LOW = 22050
        self.SAMPLE_RATE_DETECT = 48000
        self.MAX_FILE_SIZE_SEC = 60*10
        self.FILE_DETECT_CHUNK_SEC = 3
        self.MIN_FILE_SIZE_SEC = 1.5
        self.CHANNELS_STEREO = 2
        self.CHANNELS_MONO = 1
        self.LEVEL_SAMPLES = 64 # number of samples used when calculating audio level
        self.RES_HIGH = 16
        self.RES_LOW = 8
        self.BYTES_HIGH = 2
        self.BYTES_LOW = 1
        self.LEVEL_SCALE = self.LEVEL_SAMPLES / 6 # tune level when audio chart displays red
        self.RESOLUTION = 2 # 4
        self.CHART_REFRESH_RATE_MS = 250 # audio chart
        self.DETECT_INTERVAL_MS = 3000
        self.DETECT_BUFFFER_REFRESH_RATE = 80 # ms => 48000/4096 = 12 fps = 80 ms
        self.STATS_QUALITY_REFRESH_RATE = 30000 # ms => 30 secs
        self.P_DEFAULT = 0.1
        if self.THEME == "DARK":
            self.COLOR_BG = "#191919"
            self.COLOR_BG_DARK = "#191919"
        else:
            self.COLOR_BG = "#2b2b2b"
            self.COLOR_BG_DARK = "#202020"
        self.COLOR_GRID = "#2b2b2b"
        self.COLOR_LINE = "#F00"
        self.COLOR_BLUE = "#00F"
        self.COLOR_GREEN = "#0F0"
        self.COLOR_RED = "#F00"
        self.COLOR_ORANGE = "#FF7F50"
        self.COLOR_FONT = "#DDD"
        self.COLOR_FONT_DARK = "#999"
        self.LANGS = ["sv", "en", "sci"]
        self.BUTTON_HOME = "Home"
        self.BUTTON_SEARCH = "Lists"
        self.BUTTON_LIBRARY = "Detected"
        self.BUTTON_SETTINGS = "Settings"
        self.BUTTON_LOCATION = "Location"
        self.BUTTON_IMPORT = "Files"
        self.BUTTON_SHARE = "Share"
        self.BUTTON_ABOUT = "About"
        self.DIAL_FILTER_P = "Filter P"
        self.BUTTONS = [self.BUTTON_HOME, self.BUTTON_LIBRARY, self.BUTTON_SEARCH, self.BUTTON_LOCATION, self.BUTTON_SHARE, self.BUTTON_IMPORT, self.BUTTON_SETTINGS, self.BUTTON_ABOUT]
        self.DATA_COLS = ['Species', 'Quality', 'Time', 'Date', 'Country', 'Lat', 'Lon']
        self.COLOR_SCALE = ['#ff0000', '#ffa500', '#ffff00', '#008000','#008000']
        self.QUALITY_LEVELS = ["Low", "Average", "Good", "Excellent"]

        self.ICONS_FUGUE = {
                self.BUTTON_HOME: "system-monitor.png",
                self.BUTTON_SEARCH: "magnifier-zoom.png",
                self.BUTTON_LIBRARY: "tick.png",
                self.BUTTON_LOCATION: "map.png",
                self.BUTTON_SHARE: "share-balloon.png",
                self.BUTTON_SETTINGS: "gear.png",
                self.BUTTON_IMPORT: "application-import.png",
                self.BUTTON_ABOUT: "information-italic.png"
                }
        
        self.ICONS_DARK = {
                self.BUTTON_HOME: "free-circle-icon-6-2-2-0.png",
                self.BUTTON_LIBRARY: "free-circle-icon-6-2-3-0.png",
                self.BUTTON_SEARCH: "free-circle-icon-6-2-4-3.png",
                self.BUTTON_LOCATION: "free-circle-icon-6-2-5-1.png",
                self.BUTTON_SHARE: "free-circle-icon-6-2-3-1.png",
                self.BUTTON_SETTINGS: "free-circle-icon-6-2-1-6.png",
                self.BUTTON_IMPORT: "free-circle-icon-6-2-4-0.png",
                self.BUTTON_ABOUT: "free-circle-icon-6-2-4-6.png"
                }

        if self.THEME == "DARK":
            self.ICONS = self.ICONS_DARK
        else:
            self.ICONS = self.ICONS_FUGUE

    def isTest(self):
        return self.TEST



