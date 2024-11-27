import network
import time
import ubinascii
from umqtt.simple import MQTTClient
import machine
import dht

# Wi-Fi Configuration, add your Wi-Fi SSID and password here
SSID = ''
PASSWORD = ''


# MQTT Configuration, add your MQTT broker address and port here
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
# Add your unique MQTT topic for temperature here (your name + your date of birth + 'TEMP')
TOPIC_TEMP = ''  #
# Add your unique MQTT topic for humidity here (your name + your date of birth + 'HUMID')
TOPIC_HUMIDITY = ''

# Set up DHT11 sensor
dht_sensor = dht.DHT11(machine.Pin(21))  # Assuming DHT11 is connected to GPIO 21

# Function to connect to Wi-Fi
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
        print(f"Connecting to Wi-Fi... Retry {retries}/{max_retries}")
    
    if wlan.isconnected():
        # extract from the returnvalue of the wlan.ifconfig() method the IP-address 
        ip = 
        print('Connected to Wi-Fi:', ip)
        return True
    else:
        print('Failed to connect to Wi-Fi')
        return False

# Try to connect to Wi-Fi
if not connect_wifi():
    # If failed to connect, halt the program
    while True:
        time.sleep(1)

# MQTT message callback (not used in publisher)
def mqtt_callback(topic, msg):
    pass

# Connect to MQTT Broker
print("Connecting to MQTT broker...")
client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.set_callback(mqtt_callback)

try:
    client.connect()
    print('Connected to MQTT Broker:', MQTT_BROKER)

    # Publish loop
    while True:
        try:
            # Read DHT11 sensor data as float-values
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            humidity = dht_sensor.humidity()

            # Print debug info over serial
            print(f"Temperature: {temp}C, Humidity: {humidity}%")

            # Publish encoded data to both MQTT topics with the client.publish() method 
            # temperature
            # humidity
            time.sleep(5)  # Publish data every 5 seconds (adjust as needed)

        except Exception as e:
            print("Error reading DHT11 sensor:", e)
            time.sleep(2)

except Exception as e:
    print('Failed to connect to MQTT Broker:', e)

