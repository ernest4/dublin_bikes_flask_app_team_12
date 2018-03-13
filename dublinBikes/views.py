from flask import render_template

from dublinBikes import application


@application.route('/')
def index():
    application.logger.warning('sample message')
    return render_template('index.html')
