import network
import time
import ubinascii
from umqtt.simple import MQTTClient
import machine
import ssd1306

# Wi-Fi Configuration, add your Wi-Fi SSID and password here
SSID = ''
PASSWORD = ''

# MQTT Configuration, add your MQTT broker address and port here
MQTT_BROKER = ''
MQTT_PORT = 
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
# Add your unique MQTT topic for temperature here (your name + your date of birth + 'TEMP')
TOPIC_TEMP = ''
# Add your unique MQTT topic for humidity here (your name + your date of birth + 'HUMID')
TOPIC_HUMIDITY = ''


# Set up I2C for OLED
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
 
# Function to update OLED display
def update_oled(lines):
    # implement here your code:
    # 1) to clear the oled-display
    # 2) to read each element from lines 
    # 3) to write each element to the oled-display
    # 4) update the display

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()  # Disconnect in case it's already connected
    wlan.connect(SSID, PASSWORD)
    
    max_retries = 20
    retries = 0
    
    while not wlan.isconnected() and retries < max_retries:
        retries += 1
        time.sleep(1)
        # add an update_oled method to display 3 lines: "Connecting to"; "Wi-Fi"; "Retry x from 20".
        # add also a print statement with the same data (for debugging purpose) 
    
    if wlan.isconnected():
        # extract from the returnvalue of the wlan.ifconfig() method the IP-address 
        ip = 
        # add an update_oled method to display 3 lines: "Connected to Wi-Fi"; "IP:"; your.ip-address
         time.sleep(3)
        print('Connected to Wi-Fi:', wlan.ifconfig())
        return True
    else:
        # add an update_oled method to display 4 lines: "Failed to"; "connect to"; "Wi-Fi"; your SSID
        print('Failed to connect to Wi-Fi')
        return False

# Try to connect to Wi-Fi
if not connect_wifi():
    # If failed to connect, halt the program
    while True:
        time.sleep(1)

# Global variables to store the last received values
last_temp = "No Data"
last_humidity = "No Data"

# MQTT message callback
def sub_callback(topic, msg):
    global last_temp, last_humidity
    
    print((topic, msg))
    # add code here to test if the current topic is coming from your publisher and containind the TEMP-data, if so: store the decoded value in variable: last_temp 
    # add code here to test if the current topic is coming from your publisher and containind the HUMIDITY-data, if so: store the decoded value in variable: last_humidity 

    # Update OLED display with the last received values
    # add here an update_oled method to display 2 lines: "Temp: x C"; "Hum: y3 %" where x=last_temp and y=last_humidity
    oled.show()

# Connect to MQTT Broker
time.sleep(2)
client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.set_callback(sub_callback)

try:
    client.connect()
    # add here an update_oled method to display 3 lines: "Connected to MQTT"; "Broker"; MQTT_BROKER
    print('Connected to MQTT Broker:', MQTT_BROKER)

    # Subscribe to topics
    # add here an update_oled method to display 2 lines: "Subscribing to"; "topics..."
    client.subscribe(TOPIC_TEMP)
    client.subscribe(TOPIC_HUMIDITY)
    # add here an update_oled method to display 3 lines: "Subscribed to"; "topics"; "Waiting for data..."
 
    while True:
        client.check_msg()
        time.sleep(1)

except Exception as e:
    # add here an update_oled method to display 3 lines: "Failed to"; "connect to the"; "MQTT broker"
    print('Failed to connect to MQTT Broker:', e)

