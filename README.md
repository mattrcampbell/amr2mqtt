# AMR2MQTT: Send AMR/ERT Meter Data Over MQTT

##### Copyright (c) 2018 Ben Johnson. Distributed under MIT License.

Using an [inexpensive rtl-sdr dongle](https://www.amazon.com/s/ref=nb_sb_noss?field-keywords=RTL2832U), it's possible to listen for signals from ERT compatible smart meters using rtlamr. This script runs as a daemon, launches rtl_tcp and rtlamr, and parses the output from rtlamr. If this matches your meter, it will push the data into MQTT for consumption by Home Assistant, OpenHAB, or custom scripts.

## Requirements

Tested under Raspbian GNU/Linux 9.3 (stretch)

Tested under Ubuntu 18.04.4 LTS

### rtl-sdr package

Install RTL-SDR package

`sudo apt-get install rtl-sdr`

Set permissions on rtl-sdr device

/etc/udev/rules.d/rtl-sdr.rules

`SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", MODE:="0666"`

Prevent tv tuner drivers from using rtl-sdr device

/etc/modprobe.d/rtl-sdr.conf

`blacklist dvb_usb_rtl28xxu`

### git

`sudo apt-get install git`

### pip3 and paho-mqtt

Install pip for python 3

`sudo apt-get install python3-pip`

Install paho-mqtt package for python3

`sudo pip3 install paho-mqtt`

Install psutil package for python3

`sudo pip3 install psutil`

### golang & rtlamr

Install Go programming language & set gopath

`sudo apt-get install golang`

https://github.com/golang/go/wiki/SettingGOPATH

If only running go to get rtlamr, just set environment temporarily with the following command

`export GOPATH=$HOME/go`


Install rtlamr https://github.com/bemasher/rtlamr

`go get github.com/bemasher/rtlamr`

To make things convenient, I'm copying rtlamr to /usr/local/bin

`sudo cp ~/go/bin/rtlamr /usr/local/bin/rtlamr`

## Install

### Clone Repo
Clone repo into opt

`cd /opt`

`sudo git clone https://github.com/chrcraven/amr2mqtt.git`

### Configure

Copy template to settings.py

`cd /opt/amr2mqtt`

`sudo cp settings_template.py settings.py`

Edit file and replace with appropriate values for your configuration. Leave watched meters blank to discover all broadcasting meters in your area. If you want the service to wait until another process is running (ie Mosquitto MQTT) use the top command to find the process name and populate PROCESS_WAIT_TO_START.

`sudo nano /opt/amr2mqtt/settings.py`

### Install Service and Start

Copy amr2mqtt service configuration into systemd config

`sudo cp /opt/amr2mqtt/amr2mqtt.systemd.service /etc/systemd/system/amr2mqtt.service`

Refresh systemd configuration

`sudo systemctl daemon-reload`

Start amr2mqtt service

`sudo service amr2mqtt start`

Set amr2mqtt to run on startup

`sudo systemctl enable amr2mqtt.service`


### Testing

Be patient! There is a built in delay of two minutes on service startup before data starts loading into MQTT. This delay is to ensure your machine is ready post boot. Use a GUI or command line tool to view the 'readings' topic on your MQTT server. I use a tool called MQTT Explorer which offers installation packages for Linux, Windows, and Apple. Download at https://mqtt-explorer.com/

## The What and the How

###Program flow
You have made it this far and now have data feeding into your MQTT server. Now it is time to understand how this program works so you can make informed choices as to how you use this data. When amr2mqtt is run it first starts rtl_tcp, then rtlamr, and then enters into its main loop. rtlamr is set up to return SCM, SCM+, and IDM messages from broadcasting meters in a JSON format and the main loop of the program reads this JSON output from rtlamr and pushes it to MQTT using the following logic:

readings/{meter_id}/{message_type}

###Example

For example, my electric meter broadcasts both SCM and IDM messages so the following topics would have JSON messages published to them: 

readings/{my_meter}/scm 

```
{
"Time":"2020-02-17T16:42:16.121571951Z",
"Offset":0,
"Length":0,
"Type":"SCM",
"Message": {
  "ID":,
  "Type":7,
  "TamperPhy":2,
  "TamperEnc":2,
  "Consumption":974582,
  "ChecksumVal":37576
  }
}
```

readings/{my_meter}/idm

```
{
"Time":"2020-02-17T16:45:12.844042259Z",
"Offset":0,
"Length":0,
"Type":"IDM",
"Message": {
  "Preamble":,
  "PacketTypeID":28,
  "PacketLength":92,
  "HammingCode":198,
  "ApplicationVersion":4,
  "ERTType":7,
  "ERTSerialNumber":,
  "ConsumptionIntervalCount":235,
  "ModuleProgrammingState":188,
  "TamperCounters":"AgIAEgoA",
  "AsynchronousCounters":0,
  "PowerOutageFlags":"AAAAACAA",
  "LastConsumptionCount":974588,
  "DifferentialConsumptionIntervals:[6,6,5,9,10,7,5,4,8,9,9,9,5,5,6,11,13,8,5,4,6,9,8,8,7,6,4,5,4,5,5,4,3,3,7,8,8,3,5,5,4,9,12,7,4,3,3],
  "TransmitTimeOffset":15,
  "SerialNumberCRC":42424,
  "PacketCRC":11799
  }
}
```

For more information on the message types visit https://github.com/bemasher/rtlamr/wiki/Protocol

## Configure Home Assistant

To use these values in Home Assistant,
```
sensor:
  - platform: mqtt
    state_topic: "readings/12345678/scm"
    name: "Power Meter"
    unit_of_measurement: kWh
    
  ```

