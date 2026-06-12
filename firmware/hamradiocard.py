import network
import time
import requests
from machine import Pin

# https://wiki.seeedstudio.com/xiao_esp32c3_with_micropython/
# will hang until successful connection made 
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('SSID', 'KEY') #replace the ssid and key.
        # I really don't want to show my wifi password in my firmware so it's left as a placeholder for now
        while not wlan.isconnected():
            time.sleep(1) 
            pass
    print('network config:', wlan.ifconfig())

def getjson(url):
    response = requests.get(url)
    response_code = response.status_code
    print('Response code: ', response_code)
    response_data = response.json()
    response.close() 
    return response_data  

def getSpecialTagVal(data, start_tag, end_tag):
    try:
        if data.find(start_tag) == -1:
            start_ind = -1
        else: 
            start_ind = data.find(start_tag) + len(start_tag)
        end_ind = data.find(end_tag)
        
        if start_ind != -1 and end_ind != -1:
            value = data[start_ind:end_ind]
            return value
        else:
            print('Tag not found in xml response')
            return -1 
    except Exception as e:
        print('Parsing error: ', e)
        return -1 

def getTagVal(data, tag):
    start_tag = tag
    end_tag = "</" + tag[1:] 
    return getSpecialTagVal(data, start_tag, end_tag)

def getHFVal(data, r, c):
    timeOfDay = ''
    bandnames = {
        0: '80m-40m',
        1: '30m-20m',
        2: '17m-15m',
        3: '12m-10m' 
    }
    
    if r == 0:
        # Daytime
        timeOfDay = 'day'
    else:
        # Nighttime
        timeOfDay = 'night'
    
    longtag = '<band name="' + bandnames[c] + '" time="' + timeOfDay + '">'
    return getSpecialTagVal(data, longtag, '</band>') 

# Set up network connection and pins 
do_connect()

dataPin = Pin(2, Pin.OUT)
latchPin = Pin(4, Pin.OUT)
clockPin = Pin(3, Pin.OUT) 

# Loop
while True:
    # Get data 
    url = 'https://www.hamqsl.com/solarxml.php'

    k_ind = -1
    sfi = -1
    a_ind = -1
    #       80-40  30-20  17-15  12-10
    # Day  |_____|_______|______|______
    # Night|     |       |      |
    hfconditions = [
        ["", "", "", ""],
        ["", "", "", ""]
    ]

    try:
        response = requests.get(url)
        response_code = response.status_code
        print('Response code: ', response_code)
        # Text for xml 
        data = response.text 
        response.close()  
        
        if data:
            sfi = int(getTagVal(data, '<solarflux>'))
            a_ind = int(getTagVal(data, '<aindex>'))
            k_ind = int(getTagVal(data, '<kindex>'))
            
            for r in range(0, 2):
                for c in range(0, 4):
                    hfconditions[r][c] = getHFVal(data, r, c)
            
        else:
            print('No data found in solarxml.php')
    except Exception as e:
        print('An error occurred during the request: ', str(e)) 

    # Display data
    # https://wokwi.com/projects/396045549702862849
    
    #U3 - 4 for Kp and 4 empty 
    kp_disp = [0, 0, 0, 0]
    if k_ind >= 7:
        kp_disp[3] = 1
    elif k_ind >= 5:
        kp_disp[2] = 1
    elif k_ind >= 3:
        kp_disp[1] = 1
    elif k_ind <= 2:
        kp_disp[0] = 1 

    #U2 - 4 for sfi and 4 for A 
    sfi_disp = [0, 0, 0, 0]
    if sfi < 80:
        sfi_disp[0] = 1
    elif sfi < 90:
        sfi_disp[1] = 1
    elif sfi < 100:
        sfi_disp[2] = 1
    elif sfi >= 100:
        sfi_disp[3] = 1

    a_disp = [0, 0, 0, 0]
    if a_ind >= 50:
        a_disp[3] = 1
    elif a_ind >= 20:
        a_disp[2] = 1
    elif a_ind >= 10:
        a_disp[1] = 1
    elif a_ind < 10:
        a_disp[0] = 1 

    # U4 - 8 for daytime
    # U5 - 8 for nighttime 
    hf_disp = [
        [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]]
    ]

    for r in range(0, 2):
        for c in range(0, 4):
            text = hfconditions[r][c]
            if text == 'Poor':
                # Red light
                hf_disp[r][c][0] = 1
            elif text == 'Good':
                # Green light
                hf_disp[r][c][1] = 1
            elif text == 'Fair':
                # Yellow light
                hf_disp[r][c][0] = 1
                hf_disp[r][c][1] = 1 

    total = kp_disp + [0, 0, 0, 0] + sfi_disp + a_disp + [item for row in hf_disp for pair in row for item in pair]

    latchPin.off()
    for val in reversed(total):
        dataPin.value(val)
        clockPin.off()
        clockPin.on()
    latchPin.on()
    
    time.sleep_ms(600) 


    # Wait an hour
    time.sleep(60 * 60) 

