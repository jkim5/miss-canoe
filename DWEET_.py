# For use with https://freeboard.io/board/zcCWZG
# some example code: https://www.timguelke.net/blog/2018/11/17/how-to-build-a-raspberry-pi-air-quality-station
# and dweet
#
# Example dweet https://dweet.io/dweet/for/miss-canoe?latitude=44.969677&longitude=-93.301985&temperature=70.5&crew=<ul>Joe<br>Neli<br>John<br>Carlina&time=14:08:26&ph=6.99

import urllib.request
import time
import datetime

dweet_url = "https://dweet.io/dweet/for/miss-canoe?"
dweet_request = "https://dweet.io/dweet/for/miss-canoe?latitude=44.969677&longitude=-93.301985&temperature=70.5&crew=<ul>Joe<br>Neli<br>John<br>Carlina&time=14:08:26&ph=6.99"

# using dweet.io syntax
def dweet_it(request):

    x = (dweet_url + 
    "crew=" + str(request[0].crew) + "&" +
    "date=" + str(request[0].date) + "&" +
    "&time-GMT=" + str(request[0].time) + "&" +
    "latitude=" + str(request[0].latitude) + "&" +
    "longitude=" + str(request[0].longitude) + "&" +
    "alt=" + str(request[0].altitude) + "&" +
    "speed=" + str(request[0].speed) + "&" +
    "heading=" + str(request[0].heading) + "&" +
    "climb=" + str(request[0].climb) + "&" +
    "accel_x=" + str(request[0].accel_x) + "&" +
    "accel_y=" + str(request[0].accel_y) + "&" +
    "accel_z=" + str(request[0].accel_z) + "&" +
    "gyro_x=" + str(request[0].gyro_x) + "&" +
    "gyro_y=" + str(request[0].gyro_y) + "&" +
    "gyro_z=" + str(request[0].gyro_z) + "&" +
    "air_temp=" + str(request[0].air_temp) + "&" +
    "air_gas=" + str(request[0].air_gas) + "&" +
    "air_humid=" + str(request[0].air_humid) + "&" +
    "air_pressure=" + str(request[0].air_pressure) + "&" +
    "water_temp=" + str(request[0].water_temp) + "&" +
    "ysi_ph=" + str(request[0].ysi_ph) + "&" +
    "ysi_do=" + str(request[0].ysi_do) + "&" +
    "ysi_no3=" + str(request[0].ysi_no3) + "&" +
    "ysi_sal=" + str(request[0].ysi_sal) + "&" +
    "ysi_tur=" + str(request[0].ysi_tur) + "&" +
    "flow=" + str(request[0].flow))
#    "computer_date=" + str(request[0].comp_date) + "&" +
#    "computer_time=" + str(request[0].comp_time))

    print(x)
# timeout exits out of the url request in sec
    response = urllib.request.urlopen(x, timeout=1)
    html = response.read()
    response.close()  # best practice to close the file
    return()

