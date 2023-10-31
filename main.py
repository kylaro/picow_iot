import time
import network
import urequests as requests
import ujson
from leds import pulse_purple, pulse_red, pulse_green, pulse_cyan, pulse_cyan_small
from co2_sensor import read_scd41
ssid = 'Ziggo9204761'
password = 'orgxeBger9xmwGbr'
#endpoint = 'https://xhqesmfdgjqp4opmepaholks6e0zenax.lambda-url.eu-west-3.on.aws/'
endpoint = 'https://0wc4ksyc6a.execute-api.eu-west-3.amazonaws.com/PicoW'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 20
while max_wait > 0:
    pulse_cyan()
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(0.5)

# Handle connection error
if wlan.status() != 3:
    pulse_red()
    raise RuntimeError('network connection failed')
else:
    print('connected')
    pulse_purple()
    status = wlan.ifconfig()
    print('ip = ' + status[0])

while True:
    # Do things here, perhaps measure something using a sensor?
    
    
    sensor_data = read_scd41()
    if sensor_data is None:
        pulse_cyan_small()
        time.sleep(.5)
        continue # Skip this loop
    #Continue to send
    pulse_cyan()

    # Convert sensor data to JSON
    payload = ujson.dumps(sensor_data)

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY_HERE"
    }


    # Then send it in a try/except block
    try:
        print("sending...")
        response = requests.post(endpoint, headers=headers, data=payload)
        print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) )
        response.close()
    except:
        print("could not connect (status =" + str(wlan.status()) + ")")
        pulse_red()
        if wlan.status() < 0 or wlan.status() >= 3:
            print("trying to reconnect...")
            wlan.disconnect()
            wlan.connect(ssid, password)
            if wlan.status() == 3:
                print('connected')
                pulse_purple()
            else:
                pulse_red()
                print('failed')
    if response.status_code == 201:
        pulse_green()
    else:
        pulse_red()
    time.sleep(0.25)
