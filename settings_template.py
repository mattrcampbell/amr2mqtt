# List of the Meter IDs to watch
# Use empty brackets to read all meters - []
# List may contain only one entry - [12345678]
# or multiple entries - [12345678, 98765432, 12340123]
WATCHED_METERS = []

#Wait for a process to start. This can be set to the process name of the MQTT server to handle situations where the service starts prior to the MQTT server
#PROCESS_WAIT_FOR_START needs to be a string
PROCESS_WAIT_FOR_START = ''

# MQTT Server settings
# MQTT_HOST needs to be a string
# MQTT_PORT needs to be an int
# MQTT_USER needs to be a string
# MQTT_PASSWORD needs to be a string
# If no authentication, leave MQTT_USER and MQTT_PASSWORD empty
MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1883
MQTT_USER = ''
MQTT_PASSWORD = ''

# path to rtlamr
RTLAMR = '/usr/local/bin/rtlamr'

# path to rtl_tcp
RTL_TCP = '/usr/bin/rtl_tcp'
