'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template
from threading import Thread
import time
from dublinBikes import myDatabase
from datetime import datetime

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
    return "API scrapers <b>alive</b>:<br> Static: " + str(apiScarepStaticThread.is_alive()) + \
        " <br>Dynamic: " + str(apiScarepDynamicThread.is_alive()) + \
        "<br><br>Last update:<br> Static [every 24h]: " + staticAPIlastScrape + \
        " <br>Dynamic [every 5 minutes]: " + dynamicAPIlastScrape



#Scraping JCDeaux API
def scrapeAPIstatic():
    global justStarted
    global staticAPIlastScrape
    if justStarted == True: #Create a little lag between static and dynamic scrapers to prevent simultaneous write to database
        justStarted = False
        time.sleep(60*2.5)
    while True:
        staticAPIlastScrape = "Scrapping API... Populating Static data. <b>Time milis</b>: " + str(time.time()*1000) + " <b>Time</b>: " + str(datetime.fromtimestamp(time.time()))
        print(staticAPIlastScrape)
        myDatabase.populateStaticTable(myDatabase.getJCD())
        time.sleep(60*60*24) #Scrape every 24 hours
        
def scrapeAPIdynamic():
    global dynamicAPIlastScrape
    while True:
        dynamicAPIlastScrape = "Scrapping API... Populating Dynamic data. <b>Time milis</b>: " + str(time.time()*1000) + " <b>Time</b>: " + str(datetime.fromtimestamp(time.time()))
        print(dynamicAPIlastScrape)
        myDatabase.populateDynamicTable(myDatabase.getJCD())
        time.sleep(60*5) #Scrape every 5 minutes
        
        
apiScarepDynamicThread = Thread(target=scrapeAPIdynamic)
apiScarepStaticThread = Thread(target=scrapeAPIstatic)
        
def main():
    #Create and start the JCD API scraper threads for static and dynamic data scraping
    apiScarepDynamicThread.start()
    apiScarepStaticThread.start()
    
    application.run(host='0.0.0.0', port=5000, use_reloader=False)
    

if __name__ == '__main__':
    main()
    
    
    
    