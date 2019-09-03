# uses the gpsd-py3 library
# https://github.com/MartijnBraam/gpsd-py3
import gpsd
import time

# See the inline docs for GpsResponse for the available data

# Get gps position
# and error handling. gpsd.get_curent is weird and it if a NoFixError is found
# then it breaks the routine. So this is the work-around for that

def get_gps_data():

# Connect to the local gpsd
 try:
   gpsd.connect()
 except: 
   print("Error gpsd.connect()")

 try:
   packet = gpsd.get_current()
#   print_short_gps_data(packet)
#   print_all_gps_data(packet)
 except:
   print("Error gpsd.get_current()")
   packet = None
 return packet

# simple list of parameters for GPS

def print_short_gps_data(packet):
  print(packet.position())
  print("  Time: " + str(packet.time))

# full list of parameters for GPS
### See the inline docs for GpsResponse for the available data
##
##def print_all_gps_data(packet):
##
##  print(" ************ PROPERTIES ************* ")
##  print("  Mode: " + str(packet.mode))
##  print("  Satellites: " + str(packet.sats))
##
##  if packet.mode >= 2:
##    print("  Latitude: " + str(packet.lat))
##    print("  Longitude: " + str(packet.lon))
##    print("  Track: " + str(packet.track))
##    print("  Horizontal Speed: " + str(packet.hspeed))
##    print("  Time: " + str(packet.time))
##    print("  Error: " + str(packet.error))
##  else:
##    print("  Latitude: NOT AVAILABLE")
##    print("  Longitude: NOT AVAILABLE")
##    print("  Track: NOT AVAILABLE")
##    print("  Horizontal Speed: NOT AVAILABLE")
##    print("  Error: NOT AVAILABLE")
##
##  if packet.mode >= 3:
##    print("  Altitude: " + str(packet.alt))
##    print("  Climb: " + str(packet.climb))
##  else:
##    print("  Altitude: NOT AVAILABLE")
##    print("  Climb: NOT AVAILABLE")
##
##  print(" ************** METHODS ************** ")
##
##  if packet.mode >= 2:
##    print("  Location: " + str(packet.position()))
##    print("  Speed: " + str(packet.speed()))
##    print("  Position Precision: " + str(packet.position_precision()))
###       print("  Time UTC: " + str(packet.time_utc()))
###       print("  Time Local: " + str(packet.time_local()))
##    print("  Map URL: " + str(packet.map_url()))
##
##  else:
##    print("  Location: NOT AVAILABLE")
##    print("  Speed: NOT AVAILABLE")
##    print("  Position Precision: NOT AVAILABLE")
###       print("  Time UTC: NOT AVAILABLE")
###       print("  Time Local: NOT AVAILABLE")
##    print("  Map URL: NOT AVAILABLE")
##
##  if packet.mode >= 3:
##    print("  Altitude: " + str(packet.altitude()))
### print("  Movement: " + str(packet.movement()))
### print("  Speed Vertical: " + str(packet.speed_vertical()))
##  else:
##    print("  Altitude: NOT AVAILABLE")
### print("  Movement: NOT AVAILABLE")
### print(" Speed Vertical: NOT AVAILABLE")
##
##  print(" ************* FUNCTIONS ************* ")
##  print("Device: " + str(gpsd.device()))
##

 

