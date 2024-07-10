import serial, time
from datetime import datetime


#import rx
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure InfluxDB connection variables
#token = "nloTTzGPJrlM_a9MwAIGz789f5Y2tEGci5GUYfRskb1GCCRTLBbCXCRHXapQk5cHu3aYAFg1E0Qf2ysY1riTmw=="
token = "IWqHqLCDbvLwv83Hd3a66QFPwKw1m1SrFmFuIWvtzGcijDKRXuFHw6Bvk3gXd4LEJxKtD5Ly1pa2rUXphAGr3w=="
org = "IPL"
bucket = "rover2"
influxip = "192.168.1.7"
influxurl = f"http://{influxip}:8086/"
print("connecting to "+influxurl)
_client = InfluxDBClient(url=influxurl, token=token, org=org) 
_write_client = _client.write_api()

#Configure the labels for the database
measurements = {0:"CO2",1:"Therm",2:"Sound",3:"Hum",4:"Mag",5:"Sound",6:"Therm",7:"Hum",8:"NA"}
teams = {0:"Mongoose",1:"Pit Viper",2:"Music",3:"Panda",4:"Magneto",5:"Cat",6:"Daisy",7:"Gallery",8:"SYS"}
try:
    ser = serial.Serial("/dev/ttyACM0")
    while True:
        timestamp_aq = datetime.now()
        data = []
        line = str(ser.readline().strip())[2:-1]#srip off some annoying string cruft
        vals = line.split(',')
        print(f"Time: {timestamp_aq}")
        for i,val in enumerate(vals):
            L = chr(i+1+96)
            team = teams[i]
            print(f"Sensor {L} {team}: {val}".format(team=teams[i]))
            #letting influx timestamp this for m
            _write_client.write(bucket, org, [{"measurement": measurements[i], "tags": {"team": teams[i]},
                                              "fields": {"value":int(val)}}])
        time.sleep(1)
except KeyboardInterrupt:
    _write_client.__del__()
    _client.__del__()
    pass
