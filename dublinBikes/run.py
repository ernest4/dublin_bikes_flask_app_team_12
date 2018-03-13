'''
Created on 6 Mar 2018

@author: ernest
'''
from dublinBikes import application

def main():
    application.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()