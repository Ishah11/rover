import serial, time
from time import gmtime, strftime
from datetime import datetime

import smbus2
import sys

#import rx
from rx import operators as ops
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure InfluxDB connection variables
token = "<InfluxDB User Token>"
org = "<InfluxDB Org>"
bucket = "<InfluxDB Bucket>"
_client = InfluxDBClient(url="<InfluxDB URL>", token=token)
_write_client = _client.write_api(write_options=WriteOptions(batch_size=500,
                                                             flush_interval=10_000,
                                                             jitter_interval=2_000,
                                                             retry_interval=5_000,
                                                             max_retries=5,
                                                             max_retry_delay=30_000,
                                                             exponential_base=2))

#Collect data
ser = serial.Serial('/dev/ttyUSB0')
port = 1
address = 0x77
bus = smbus2.SMBus(port)

#bme280.load_calibration_params(bus,address)

#Configure the labels for the database
measurement = "rpi-bme280"
location = "<location>"

try:
    while True:
        now = datetime.now()
        timestamp_aq = datetime.timestamp(now)
        iso = datetime.utcnow()
        data = []
        file1 = open('sampleData.txt', 'r')
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
            #print("[%s] Temp: %s, Humidity: %s, Pressure: %s, Air_Quality_pmtwofive: %s, Air_Quality_pmten: %s" % (iso, temperature, humidity, pressure, pmtwofive, pmten))

            find = line.split(", ")
            temperature = float(find[2])
            humidity = float(find[1])
            pressure = float(find[3])
            pmten = float(find[4])

            _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location},
                                              "fields": {"temperature": temperature}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"humidity": humidity}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"air-pressure": pressure}, "time": iso}])
            _write_client.write(bucket, org, [{"measurement":measurement, "tags": {"location": location},
                                              "fields":{"aq-pmten": pmten}, "time": iso}])
        time.sleep(10)

except KeyboardInterrupt:
    _write_client.__del__()
    _client.__del__()
    pass
