'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table

application = Flask(__name__)
application.debug = False
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #local testing
# dialect+driver: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)
#application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/dublinbike' #AWS RDB (external)
#db = SQLAlchemy(application)

engine = create_engine('mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/pets', convert_unicode=True)
metadata = MetaData(bind=engine)
users = Table('cats', metadata, autoload=True)
#print(users.select(users.c.id == 1).execute().first())
result = list(engine.execute('select * from cats'))

for row in result:
    print(row)

catsDict = {'allcats' : result}
print(catsDict['allcats'])

@application.route('/')
def index():
    return render_template('index.html', **catsDict)

@application.route('/<yourName>')
def indexName(yourName):
    return "Your name is: " + yourName

@application.route('/station', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def stationRequest():
    if request.method == 'GET' and 'station' in request.args:
        return "You selected station (GET result): " + request.args['station']
    elif request.method == 'POST' and 'station' in request.form:
        return "You selected station (POST result): " + request.form['station']
    else:
        return "No station selected!"

def main():
    application.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
    
    
    
    