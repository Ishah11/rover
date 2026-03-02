This is a collection of scripts used to build a quick draft of an "exploration" rover. The rover can be outfitted with sensors read out through an arduino ADC.  Downlink and uplink through a wifi router using ssh for drive, HTTP streaming for HAZCAM and HTTP post for data.

## Parts:
 - Raspberry Pi 4
 - battery with 5 and 12V outputs
 - rocker bogie frame with 6 wheels driven by geared brushed motors
 - two output H bridge, one output drives three wheels on a side
 - arduino board for sensor inputs
 - usb camera "HAZCAM"
 - dedicated wifi router with admin access
 - data server running influx and grafana

## Contents of this repo
 - Drive code - latest is simpledrive2.py To drive, log in over ssh and execute.
 - serial2influx.py which converts serial data to be plotted on influxdb
 - telemetrytest.py generates telemetry to test data
 - sensorreadings.py reads sensor data from arduino
 - Basic streaming Arduino digitizer
