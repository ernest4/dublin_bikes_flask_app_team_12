'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template
from threading import Thread
import time
from dublinBikes import myDatabase
from datetime import datetime

import sys

#global vars
justStarted = True #global var indicating if this the server has just started
dynamicAPIlastScrape = ""
staticAPIlastScrape = ""

application = Flask(__name__)
application.debug = False

@application.route('/') #Render the main page
def index():
    return render_template('index.html')

@application.route('/jcdapi', methods = ['GET']) #Provide the JCD API JSON to front end
def jcdAPItoFrontEnd():
    return application.response_class(response=myDatabase.query(), status=200, mimetype='application/json')

@application.route("/api") #For debugging, check the JCD API scraper status
def status():
    return "API scrapers <b>alive</b>: " + str(apiScarepThread.is_alive()) + \
        "<br><br>Last update:<br> Static [every 24h]: " + staticAPIlastScrape + \
        " <br>Dynamic [every 5 minutes]: " + dynamicAPIlastScrape



#Scraping JCDeaux API
def scrapeJCDAPI():
    global justStarted
    global staticAPIlastScrape
    global dynamicAPIlastScrape
    
    scrapeCount = 0
    
    while True: #Run for as long as the server is active...
        
        jcdAPIquery = myDatabase.getJCD()
        if scrapeCount == 288 or justStarted == True: # Run when server launches. Then about every 24h...
            justStarted = False
            scrapeCount = 0
            staticAPIlastScrape = "Scrapping API... Populating Static data. <b>Time milis</b>: " + str(time.time()*1000) + " <b>Time</b>: " + str(datetime.fromtimestamp(time.time()))
            print(staticAPIlastScrape)
            myDatabase.populateStaticTable(jcdAPIquery)
        else: # Run about every 5 minutes...
            scrapeCount += 1
            dynamicAPIlastScrape = "Scrapping API... Populating Dynamic data. <b>Time milis</b>: " + str(time.time()*1000) + " <b>Time</b>: " + str(datetime.fromtimestamp(time.time()))
            print(dynamicAPIlastScrape)
            myDatabase.populateDynamicTable(jcdAPIquery)
            
        time.sleep(60*5) #Scrape about every 5 minutes...
            
            
apiScarepThread = Thread(target=scrapeJCDAPI)
        
def main():
    #Create and start the JCD API scraper thread for static and dynamic data scraping
    apiScarepThread.start()
    
    inputStr = input("Is this running on localhost [y/n]: ").lower()
    if inputStr == "yes" or inputStr == "y": #Running on laptop/desktop
        application.run(host='0.0.0.0', port=5000, use_reloader=False)
    elif inputStr == "no" or inputStr == "n": #Running on EC2
        application.run(host='0.0.0.0', port=80, use_reloader=False)
    else:
        print("Invalid input, exiting...")
        sys.exit()
    

if __name__ == '__main__':
    main()
    
    
    
    