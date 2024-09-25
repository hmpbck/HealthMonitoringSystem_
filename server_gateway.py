from flask import Flask, render_template
import serial
import json

app = Flask(__name__)

# Change 'COM3' to your Arduino's serial port
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600

@app.route('/')
def index():
    # Read data from Arduino serial port
    data = read_serial_data()
    return render_template('index.html', data=data)

def read_serial_data():
    data = {}
    try:
        # Open serial port
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # Read line from serial port
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:  # If there's data
                    json_data = json.loads(line)
                    # Store data using unique ID
                    data[json_data['id']] = {
                        'temperature': json_data['temperature'],
                        'humidity': json_data['humidity'],
                        'pulse': json_data['pulse']
                    }
                break  # Exit after reading one line
    except Exception as e:
        print(f"Error reading serial data: {e}")
    return data

if __name__ == '__main__':
    app.run(debug=True)
