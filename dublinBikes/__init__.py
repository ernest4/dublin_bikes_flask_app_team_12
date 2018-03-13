import os
from flask import Flask

application = Flask(__name__)
application.config.from_object('dublinBikes.default_settings')
#app.config.from_envvar('DUBLINBIKES_SETTINGS')

if not application.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(application.config['LOG_DIR'], 'dublinBikes.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    application.logger.addHandler(file_handler)

import dublinBikes.views
