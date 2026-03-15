#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.insert(0,"./site-packages/exoplanets/")


from observatory import Observatory
from sun import SolarTwilight
from astropytime import getIers
from timegraph import TimeGraph
from generatehtmlpage import HtmlPageGenerator
from objectofinterest import TransitInfo, ListObjectOfInterest, ObjectOfInterest
import os
import glob

#from astropy import units as u
#from astropy.coordinates import SkyCoord, FK5
#import numpy as np
#from astropy.time import Time
import datetime

#iers_a = getIers()


start_date=datetime.datetime(2026,3,1)
end_date  =datetime.datetime(2026,3,10)

def daterange(start_date, end_date):
 for n in range(int ((end_date - start_date).days)):
  yield start_date + datetime.timedelta(n)


if __name__ == "__main__":


 listObjectOfInterest =  ListObjectOfInterest()
 listObjectOfInterest.parseCsvFile( "obj.dat" )
 #listObjectOfInterest.parseXmlFile( "WASP-107.xml" )
 #listObjectOfInterest.parseXmlFile( "WASP-48.xml" )
 print( listObjectOfInterest )

# observatory = Observatory("crimea")
 observatory = Observatory("saoras")
# observatory = Observatory("india_1.3m")

 if not os.path.exists( observatory["shortname"] ):
  os.mkdir( observatory["shortname"] )
 os.chdir( observatory["shortname"] )
 
 htmlPageGenerator = HtmlPageGenerator( observatory )
 for single_date in daterange(start_date, end_date):
  dateOfInterest = single_date.strftime("%Y-%m-%d")
  print( dateOfInterest )
  solarTwilight = SolarTwilight(observatory, dateOfInterest)
  listObjectOfInterest.calculateTransits( solarTwilight, observatory )
  listObjectOfInterest.sortObject()

  timeGraph = TimeGraph(solarTwilight)
  htmlPageGenerator.middle(dateOfInterest, listObjectOfInterest, solarTwilight.changeTo(), observatory)
  for objectOfInterest in listObjectOfInterest:
   for transitInfo in objectOfInterest["transitsList"]:
    if transitInfo["isNight"]:
     print( objectOfInterest, transitInfo )
     timeGraph.plotObject(objectOfInterest, transitInfo, observatory, solarTwilight)

  timeGraph.plotAfter(dateOfInterest)
 htmlPageGenerator.writeto( "index2026.{}.html".format(observatory["shortname"]) )
