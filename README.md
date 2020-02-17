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

Edit file and replace with appropriate values for your configuration. Leave watched meters blank to discover all broadcasting meters in your area.

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

Use a GUI or command line tool to view the 'readings' topic. I prefer to use a tool called MQTT Explorer which offers installation packages for Linux, Windows, and Apple. Download at https://mqtt-explorer.com/

## The What and the How

You have made it this far and now have data feeding into your MQTT server.

## Configure Home Assistant

To use these values in Home Assistant,
```
sensor:
  - platform: mqtt
    state_topic: "readings/12345678/scm"
    name: "Power Meter"
    unit_of_measurement: kWh
    
  ```

