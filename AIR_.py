import time
import board
from busio import I2C
import adafruit_bme680

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
# bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
# bme680.sea_level_pressure = 1013.25

def show_air_readings(air_temp, air_gas, air_humid, air_pressure):

    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
    bme680.sea_level_pressure = 1013.25

    air_temp = bme680.temperature
    air_gas = bme680.gas
    air_humid = bme680.humidity
    air_pressure = bme680.pressure
    return(air_temp, air_gas, air_humid, air_pressure)

# while True:
#    print("\nTemperature: %0.1f C" % bme680.temperature)
#    print("Gas: %d ohm" % bme680.gas)
#    print("Humidity: %0.1f %%" % bme680.humidity)
#    print("Pressure: %0.3f hPa" % bme680.pressure)
#    print("Altitude = %0.2f meters" % bme680.altitude)

#    time.sleep(1)


