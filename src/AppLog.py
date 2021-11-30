import logging
from AppConfig import FileConfig

class Log():
    def __init__(self):
        logging.basicConfig()
        level = FileConfig().LOGGING["level"]
        levels = {"debug": logging.DEBUG, "info": logging.INFO}
        self.log = logging.getLogger("birdify")
        self.log.setLevel(levels[level])

    def debug(self, msg):
        self.log.debug(msg)

    def info(self, msg):
        self.log.info(msg)