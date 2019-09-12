"""
==================================
2019 09 04
* Started the process of adding significant comments throughout.
* Include credits.

2019 09 03

NEED TO COMMENT THIS CODE FOR SHARING!
NOTES
* Crontab integration for starting the service during reboot
    * There needs to be a pause for system startup for crontab to work with this program. I've implement a 10 sec delay, which seems to work.

STILL TO DO
* Error handling - tricky as errors in libraries tend to break the code 
* Move code to Github, especially noting Issues

Author(s): John Kim <jkim5@macalester.edu>, Anthony Tran <anthony.d.tran@gmail.com>
Based on other peoples work throughout. Adding credits throughout.

==================================
"""
# Import python modules
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# IMPORTANT need to pause for crontab job for all computer services to start. 
# 10 sec seems to work.
# Move this
time.sleep(0)

# Import my modules
from GPS_ import *
from DWEET_ import *
from OLED_ import *
from DOF_ import *
from AIR_ import *
from WATERTEMP_ import *
# from READFILE_ import *
# from FTP_ import *

# Constants
crew = None   # <> separate these, as commas are used for CSV. Make this a separate file so I don't go into this code.
home = "/home/pi/Code/miss-canoe/"
log_file = "log.txt"
crew_file = "crew_list.txt"
freq_cycles = 2            # used for frequency of data collection (in seconds)
freq_upload = 2              # freq of ftp uploads (in hours; .5 = 30 min)
# num_cycles = freq_upload * (3600 / freq_cycles)        # works with freq_upload. Calculates num_cycles based on freq_upload. Do not change. 0 = every cycle
startup_pause = 2         # how long to pause at startup to display IP info

# Object definition for data measurement
class data:
    def __init__(self, index=0, crew=None, date=None, time=None, latitude=None, longitude=None, altitude=0.0, speed=0.0, heading=0.0, climb=0.0, accel_x=0.0, accel_y=0.0, accel_z=0.0, gyro_x=0.0, gyro_y=0.0, gyro_z=0.0, air_temp=0.0, air_gas=0.0, air_humid=0.0, air_pressure=0.0, water_temp=0.0, ysi_ph=0.0, ysi_do=0.0, ysi_no3=0.0, ysi_sal=0.0, ysi_tur=0.0, flow=0.0, comp_date=None, comp_time=None, timer=0):
        self.index = 0
        self.crew = crew
        self.date = date
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.speed = speed
        self.heading = heading
        self.climb = climb
        self.accel_x = accel_x
        self.accel_y = accel_y
        self.accel_z = accel_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.air_temp = air_temp	# from air sensor; in Centigrade
        self.air_gas = air_gas		# from air sensor; in ohm
        self.air_humid = air_humid	# from air sensor; in percent
        self.air_pressure = air_pressure	# from air sensor; in hPa
        self.water_temp = water_temp
        self.ysi_ph = ysi_ph     # YSI not part of device; will integrate manually
        self.ysi_do = ysi_do
        self.ysi_no3 = ysi_no3
        self.ysi_sal = ysi_sal
        self.ysi_tur = ysi_tur
        self.flow = flow       # flow not part of device; will integrate manually
        self.comp_date = comp_date  # computer date as back-up in case of GPS failure
        self.comp_time = comp_time   # computer time as back-up in case of GPS failure. keep at end
        self.timer = timer # running timer

# -------SUBROUTINES-------------------------
# Parse up system date and time and re-format
# important to keep system date and time for file management (GPS data not 100% reliable)
def datetime_format(timenow):

    now = timenow
    mm = str(now.month)
    dd = str(now.day)
    yyyy = str(now.year)
    hour = str(now.hour)
    mi = str(now.minute)
    ss = str(now.second)
    timenow = yyyy + mm + dd + " " + hour + ":" + mi + ":" + ss
    return(timenow)

# Parse up just date and re-format. Could be integrated with previous. Bah
def date_format(timenow):

    # format month and day so double digits (leading 0 if single digit)
    tempmm = '%02d' % timenow.month
    tempdd = '%02d' % timenow.day
    mm = str(tempmm)
    dd = str(tempdd)
    yyyy = str(timenow.year)
    timenow = yyyy + mm + dd
    return(timenow)

# parse GPS date/time format
def gps_date_format(timenow):

# GPS date/time format: 2016-08-05T01:51:44.000Z
    x = timenow[0:10]
    return(x)

def gps_time_format(timenow):

# GPS date/time format: 2016-08-05T01:51:44.000Z
    x = timenow[11:22]
    return(x)

# Because raspberry pi does not have a onboard clock, set time to gps time if there's a discrepency
def set_gpstime(data):
   if (data[0].date != None):
     temp_gps_datetime_str = data[0].date + " " + data[0].time
     temp_gps_datetime = time.strptime(temp_gps_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
     if (temp_gps_datetime != None):
       if (temp_gps_datetime != datetime.datetime.now()):
          temp_cmd = "sudo date -s " + "'" + temp_gps_datetime_str + "'" # prints to screen new datetime
          # print(temp_cmd)
          os.system(temp_cmd)

# Set up write to file 
def write_to_file(data):
    try:
        todays_log_filename =  home + (str(date_format(datetime.datetime.today()) + "-data" + log_file))
        print("writing to: " + todays_log_filename + "\n")
        file = open(todays_log_filename, "a")
        x = (
          str(data[0].index) + ", " + 
          str(data[0].crew) + ", " + 
          str(data[0].date) + ", " + 
          str(data[0].time) + ", " + 
          str(data[0].latitude) + ", " + 
          str(data[0].longitude) + ", " + 
          str(data[0].altitude)+ ", " + 
          str(data[0].speed) + ", " + 
          str(data[0].heading) + ", " + 
          str(data[0].climb) + ", " +
          str(data[0].accel_x) + ", " +
          str(data[0].accel_y) + ", " +
          str(data[0].accel_z) + ", " +
          str(data[0].gyro_x) + ", " +
          str(data[0].gyro_y) + ", " +
          str(data[0].gyro_z) + ", " +
          str(data[0].air_temp) + ", " +
          str(data[0].air_gas) + ", " +
          str(data[0].air_humid) + ", " +
          str(data[0].air_pressure) + ", " +
          str(data[0].water_temp) + ", " +
          str(data[0].ysi_ph) + ", " +
          str(data[0].ysi_do) + ", " +
          str(data[0].ysi_no3) + ", " +
          str(data[0].ysi_sal) + ", " +
          str(data[0].ysi_tur) + ", " +
          str(data[0].flow) + "," +
          str(data[0].timer) +
          "\n")
# computer time is wrong because of no hardware clock. do not write.
#          str(data[0].comp_date) + ", " +
#          str(data[0].comp_time) +
#          "\n")
        #print(x)
        file.write(x)
        file.close()
    except:
        msg_handler("ERROR: write_to_file()", "") # msg_handler takes two text messages for OLED

def read_crew():
    tmploc = home + crew_file
    file2 = open(tmploc, "r")
    crew = file2.readline()

    # there is a trailing character at the end of the line. Can't tell what it is so removing.
    lenx = len(crew) - 1
    crew = crew[0:lenx]
    file2.close()
    return(crew)

# Message handling: writes to both file and OLED screen
# Receives two lines of text, because there are two additional lines of OLED
def msg_handler(str2, str3):
    
# write error to OLED screen
    show_OLED_message(str2, str3)

# write error to a log file
    now = datetime.datetime.now()
    msg = (datetime_format(now) + " " + str2 + "\n")
    print("\n" + msg)
    tmploc = home + log_file
    file = open(log_file, "a")
    file.write(msg)
    file.close()

def log_handler(str2):
    now = datetime.datetime.now()
    msg = (datetime_format(now) + " " + str2 + "\n")
    print(msg)
    file = open(log_file, "a")
    file.write(msg)
    file.close()


## end of definition of subroutines

## ______________MAIN PROGRAM_____________
        

# Startup 

# cycles = 0   # used for timing of FTP uploads / once per num_cycles

# Display local IP for testing purposes
f = os.popen('hostname -I')
iptext = "IP: " + f.read()
msg_handler("Started main_.py", iptext)
time.sleep(startup_pause)

# Read in crew list
crew = read_crew()

# Clear OLED display after sleep
# disp.fill(0)
# disp.show()

# Initialize a scheduler
sched = BlockingScheduler({
    'apscheduler.job_defaults.max_instances': '8'
})

def log_data():
    timer = int(time.time()) # running timer for purposes of tracking time without accurate time

# initialize new data object
    incoming_data = []
    incoming_data.append(data()) # this seems incorrect; find better syntax

# collect all data before putting it into the data object
#
# GPS 
# GPS needs to be on and running for this work
# still figuring out how gpsd works (esp how the program retrieves data), so this is an unforunate workaround for ensuring data is coming in

    gps_date = None
    gps_time = None
    gps_longitude = None
    gps_latitude = None
    gps_altitude = None
    gps_speed = None
    gps_heading = None
    gps_climb = None

    try:
      packet = get_gps_data()
      gps_date = gps_date_format(packet.time)
      gps_time = gps_time_format(packet.time)
      gps_latitude = packet.lat
      gps_longitude = packet.lon
      gps_altitude = packet.alt
      gps_speed = packet.hspeed
      gps_heading = packet.track
      gps_climb = packet.climb
    except:
      msg_handler("ERROR: get_gps_data()", "main_.py")

# check for a GPS errors (no fix, no)
    if (packet == None):
      msg_handler("ERROR: GPS packet = None", "main_.py")
    elif (gps_latitude == 0):
      gps_date = None
      gps_time = None
      gps_longitude = None
      gps_latitude = None
      gps_altitude = None
      gps_speed = None
      gps_heading = None
      gps_climb = None
      msg_handler("ERROR: no GPS fix", "main_.py")

    else:
      disp.fill(0)
      disp.show()

# DOF: acceleromoeter and gyroscope readings
    accel_x = 0
    accel_y = 0
    accel_z = 0
    gyro_x = 0
    gyro_y = 0
    gyro_z = 0

    try:
      accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = show_dof_readings(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
    except:
      msg_handler("ERROR: DOF reading", "main_.py")

# AIR readings
    air_temp = 0
    air_gas = 0 
    air_humid = 0
    air_pressure = 0

    try: 
      air_temp, air_gas, air_humid, air_pressure = show_air_readings(air_temp, air_gas, air_humid, air_pressure)
    except:
      msg_handler("ERROR: AIR reading", "main_.py")

# WATER temperature readings
    try:
      water_temp = read_temp()
    except:
      water_temp = 0.0
      msg_handler("ERROR: WATER TEMP reading", "main_.py")


# Append data into
    incoming_data[0].crew = crew
    incoming_data[0].date = gps_date
    incoming_data[0].time = gps_time
    incoming_data[0].latitude = gps_latitude
    incoming_data[0].longitude = gps_longitude
    incoming_data[0].altitude = gps_altitude
    incoming_data[0].speed = gps_speed
    incoming_data[0].heading = gps_heading
    incoming_data[0].climb = gps_climb
    incoming_data[0].accel_x = accel_x
    incoming_data[0].accel_y = accel_y
    incoming_data[0].accel_z = accel_z
    incoming_data[0].gyro_x = gyro_x
    incoming_data[0].gyro_y = gyro_y
    incoming_data[0].gyro_z = gyro_z
    incoming_data[0].air_temp = air_temp
    incoming_data[0].air_gas = air_gas
    incoming_data[0].air_humid = air_humid
    incoming_data[0].air_pressure = air_pressure
    incoming_data[0].water_temp = water_temp
    incoming_data[0].comp_date = str(datetime.datetime.now().date()) # keep at end
    incoming_data[0].comp_time = str(datetime.datetime.now().time())
    incoming_data[0].timer = str(timer)

# DWEET integration
# working... needs error handling integration
    try:
        dweet_it(incoming_data)
    except:
        msg_handler("ERROR: dweet_it()", "internet?")

# WRITE append and save data to file
    try:
        write_to_file(incoming_data)
    except:
        msg_handler("ERROR: write_to_file()", "main_.py")

# FTP
# Not implemented. Used a server-side handling of Dweets.
# FTP upload file at set intervals set by constant num_cycles
# todays_log_filename is a global variable
# if statement need to upload once every period

#    if (cycles >= num_cycles):
#      ftp_upload(todays_log_filename)
#      log_handler("FTP uploaded: " + todays_log_filename)
#      cycles = 0 # reset cycle count

# SET TIME TO GPS TIME.
# because when there is no internet, pi does not update time. set time from GPS
    set_gpstime(incoming_data)

# Scheduler interval
<<<<<<< HEAD
# sched.add_job(log_data, 'interval', minutes=1)
=======
>>>>>>> d4a4549ea7667dd4251037a8da37786a0acc7bf9
sched.add_job(log_data, 'interval', seconds=1)
sched.start()

try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(5)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    sched.shutdown()
