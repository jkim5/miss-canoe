# For use with https://freeboard.io/board/zcCWZG
# some example code: https://www.timguelke.net/blog/2018/11/17/how-to-build-a-raspberry-pi-air-quality-station
# and dweet
#

import urllib.request
from urllib.error import HTTPError, URLError
import time
import datetime

url_timeout = 1
dweet_url = "https://dweetpro.io/dweet/for/miss-canoe?"
gc_url = "https://us-central1-miss-anthro.cloudfunctions.net/endpoint?"
# dweet_request = "https://dweet.io/dweet/for/miss-canoe?latitude=44.969677&longitude=-93.301985&temperature=70.5&crew=<ul>Joe<br>Neli<br>John<br>Carlina&time=14:08:26&ph=6.99"

# using dweet.io syntax
def dweet_it(request):
    params = ("crew=" + str(request[0].crew) + "&" +
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
    "flow=" + str(request[0].flow) + "&" +
    "timer=" + str(request[0].timer))

#    "computer_date=" + str(request[0].comp_date) + "&" +
#    "computer_time=" + str(request[0].comp_time))
    print(params)
    
    urls = [
        '{}{}'.format(dweet_url, params), 
        '{}{}'.format(gc_url, params)
    ]

    for url in urls:
        # time.sleep(0.1)
        try:
            # timeout exits out of the url request in sec
            response = urllib.request.urlopen(url, timeout=url_timeout)
            html = response.read()
            # time.sleep(0.1)
            # best practice to close the file
            response.close()
        except (HTTPError, URLError) as e:
            print(e.reason)
            continue
    return()

