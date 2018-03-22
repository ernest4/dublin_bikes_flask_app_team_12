'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template, request
from multiprocessing import Process
from threading import Thread
import time

application = Flask(__name__)
application.debug = False

@application.route('/')
def index():
    return render_template('index.html', allcats="No cats")

LEFT, RIGHT, UP, DOWN, RESET = "left", "right", "up", "down", "reset"
AVAILABLE_COMMANDS = {'Left': LEFT, 'Right': RIGHT, 'Up': UP, 'Down': DOWN, 'Reset': RESET }
@application.route('/buttons')
def execute():
    return render_template('asyncbuttons.html', commands=AVAILABLE_COMMANDS)

@application.route('/buttons/<cmd>')
def command(cmd=None):
    if cmd == RESET:
        camera_command = "X"
        response = "(This is from server) Resetting ..."
    else:
        camera_command = cmd[0].upper()
        response = "(This is from server) Moving {}".format(cmd.capitalize())

    return response, 200, {'Content-Type': 'text/plain'}
    #return response

@application.route('/station', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def stationRequest():
    if request.method == 'GET' and 'station' in request.args:
        return "You selected station (GET result): " + request.args['station']
    elif request.method == 'POST' and 'station' in request.form:
        return "You selected station (POST result): " + request.form['station']
    else:
        return "No station selected!"

def main():
    application.run(host='0.0.0.0', port=5000, use_reloader=False)



def scrapeAPI():
    while True:
        print("Scrapping API...",time.time())
        time.sleep(60*5)

@application.route("/api")
def status():
    return "API scraper alive: " + str(apiScarepThread.is_alive())

if __name__ == '__main__':
    apiScarepThread = Thread(target=scrapeAPI)
    apiScarepThread.start()
    
    main()
    
    
    
    