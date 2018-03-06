'''
Created on 6 Mar 2018

@author: ernest
'''
import os
from dublinBikes import app

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()