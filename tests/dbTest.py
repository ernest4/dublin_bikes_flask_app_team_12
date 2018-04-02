'''
Created on 26 Mar 2018

@author: naomiwang
'''
import pytest
from dublinBikes.myDatabase import getJCD,populateDynamicTable

def testGetJCD():
    getJCD()

def testPopulateDynamicTable():
    populateDynamicTable(getJCD())
    
testPopulateDynamicTable()
#testGetJCD()
