'''
Created on 26 Mar 2018

@author: naomiwang
'''
from dublinBikes.myDatabase import getJCD,populateDynamicTable,populateStaticTable,query,weeklyAvailableBikes

def testGetJCD():
    assert getJCD()

def testPopulateStationTable():
    assert populateStaticTable(getJCD()) == None
    
def testPopulateDynamicTable():
    assert populateDynamicTable(getJCD()) == None

def testQuery():
    assert query()
    
def testWeekly():
    assert weeklyAvailableBikes(42)




    
#testPopulateDynamicTable()
#testGetJCD()
