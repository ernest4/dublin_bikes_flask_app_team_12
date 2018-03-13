'''
Created on 6 Mar 2018

@author: ernest
'''
from flask import Flask, render_template

application = Flask(__name__)
application.debug = False

@application.route('/')
def index():
    return render_template('index.html')

def main():
    application.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()