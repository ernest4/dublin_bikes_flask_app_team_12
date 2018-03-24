'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template, request
from threading import Thread
import time
from dublinBikes import myDatabase
from datetime import datetime

justStarted = True #global var indicating if this the server has just started

application = Flask(__name__)
application.debug = False

@application.route('/test')
def jcdAPItoFrontEnd():
    return myDatabase.query()

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

#Scraping JCDeaux API
def scrapeAPIstatic():
    global justStarted
    if justStarted == True: #Create a little lag between static and dynamic scrapers to prevent simultaneous write to database
        justStarted = False
        time.sleep(60*2.5)
    while True:
        print("Scrapping API... Populating Static data. Time milis:",time.time()*1000,"Time: ", datetime.fromtimestamp(time.time()))
        myDatabase.populateStaticTable()
        time.sleep(60*60*24) #Scrape every 24 hours
        
def scrapeAPIdynamic():
    while True:
        print("Scrapping API... Populating Dynamic data. Time milis:",time.time()*1000,"Time: ", datetime.fromtimestamp(time.time()))
        myDatabase.populateDynamicTable()
        time.sleep(60*5) #Scrape every 5 minutes

@application.route("/api")
def status():
    return "API scrapers <b>alive</b>:<br> Static: " + str(apiScarepStaticThread.is_alive()) + \
        " <br>Dynamic: " + str(apiScarepDynamicThread.is_alive())
        
def main():
    application.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    #Create and start the JCD API scraper threads for static and dynamic data scraping
    apiScarepDynamicThread = Thread(target=scrapeAPIdynamic)
    apiScarepDynamicThread.start()
    apiScarepStaticThread = Thread(target=scrapeAPIstatic)
    apiScarepStaticThread.start()
    
    main()
    
    
    
    