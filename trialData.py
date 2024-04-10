import serial, time
from time import gmtime, strftime
from datetime import datetime

import smbus2
import sys

#import rx
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure InfluxDB connection variables
token = "nloTTzGPJrlM_a9MwAIGz789f5Y2tEGci5GUYfRskb1GCCRTLBbCXCRHXapQk5cHu3aYAFg1E0Qf2ysY1riTmw=="
org = "rover"
bucket = "pi-rover"
_client = InfluxDBClient(url="http://localhost:8086/", token=token) 
#change client to 192.168.1.5 inplace of local host for any other pis over the rover network
_write_client = _client.write_api()

#Collect data
# ser = serial.Serial('/dev/ttyUSB0')
# port = 1
# address = 0x77
# bus = smbus2.SMBus(port)

#bme280.load_calibration_params(bus,address)

#Configure the labels for the database
measurement = "rpi-bme280"
location = "rpi"

try:
    while True:
        now = datetime.now()
        timestamp_aq = datetime.timestamp(now)
        iso = datetime.utcnow()
        data = []
        file1 = open('/home/pi/Documents/sampleData.txt', 'r')
        Lines = file1.readlines()
 
    # Strips the newline character
        for line in Lines:
            
           # datum = ser.read()
           # data.append(datum)
            #pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
            #pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') /10
            #bme280_data = bme280.sample(bus,address)
            #temperature = bme280_data.temperature
            #pressure = bme280_data.pressure
            #humidity = bme280_data.humidity
            
           # Print for debugging, uncomment the below line

            find = line.split(", ")
            temperature = float(find[2])
            humidity = float(find[1])
            pressure = float(find[3])
            pmten = float(find[4])
            print("[%s] Temp: %s, Humidity: %s, Pressure: %s,Air_Quality_pmten: %s" % (iso, temperature, humidity, pressure, pmten))

            _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location},
                                              "fields": {"temperature": temperature}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"humidity": humidity}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"air-pressure": pressure}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"aq-pmten": pmten}, "time": iso}])

except KeyboardInterrupt:
    _write_client.__del__()
    _client.__del__()
    pass
