import serial
from flask import Flask, request

app = Flask(__name__)

weight = 0
height = 0
is_mobile_connected = False
is_person_on_scale = False
is_kiosk_on = False
battery_status = 100
on_time = None
off_time = None

port = serial.Serial('COM1', baudrate=9600)

@app.route('/take-test', methods=['POST'])
def handle_take_test_request():
    global is_person_on_scale
    if is_person_on_scale:
        send_height_and_weight()
    else:
        print('Please step on the weigh scale')
    return '', 200

@app.route('/send-battery-status', methods=['POST'])
def handle_battery_status():
    global battery_status
    battery_status = request.json['batteryStatus']
    print(f'Battery Status: {battery_status}%')
    return '', 200

@app.route('/send-on-time', methods=['POST'])
def handle_on_time():
    global on_time
    on_time = request.json['onTime']
    print(f'On Time: {on_time}')
    return '', 200

@app.route('/send-off-time', methods=['POST'])
def handle_off_time():
    global off_time
    off_time = request.json['offTime']
    print(f'Off Time: {off_time}')
    return '', 200

@app.route('/send-message', methods=['POST'])
def handle_message():
    print('Received message from the mobile device')
    # Perform necessary actions based on the message received
    # ...
    global is_kiosk_on
    is_kiosk_on = False
    return '', 200

def on_data_received(data):
    global weight, is_person_on_scale
    weight_data = float(data)
    if not isnan(weight_data):
        weight = weight_data
        if not is_person_on_scale:
            is_person_on_scale = True
            print('Person is on the weigh scale')
            if is_mobile_connected:
                send_height_and_weight()
            else:
                print('Please step on the weigh scale')

def send_height_and_weight():
    # Send height and weight data to the mobile device using the appropriate method
    # ...
    print(f'Height: {height} cm, Weight: {weight} kg')

def power_on_kiosk():
    global is_kiosk_on
    is_kiosk_on = True
    print('Kiosk powered on')
    # Show "Welcome" screen on the kiosk display
    # ...
    if is_mobile_connected:
        print('Please touch screen to check your health status')
    else:
        print('Welcome to Sunya Health Kiosk')

def schedule_power_off(time):
    import datetime
    scheduled_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.datetime.now()
    time_difference = scheduled_time - current_time
    if time_difference.total_seconds() > 0:
        print(f'Kiosk will be powered off in {time_difference.total_seconds() / 60} minutes')
        import threading
        threading.Timer(time_difference.total_seconds(), power_off_kiosk).start()
    else:
        power_off_kiosk()

def power_off_kiosk():
    global is_kiosk_on
    is_kiosk_on = False
    print('Kiosk powered off')
    # Perform necessary actions to power off the kiosk
    # ...

# Set up the serial port for communication with the weigh scale
port = serial.Serial('COM1', baudrate=9600)
port.readline()
port.close()
port.open()
port.on_data_received = on_data_received

# Set up the Flask server for mobile communication
if __name__ == '__main__':
    app.run()

# Power on the kiosk
power_on_kiosk()
