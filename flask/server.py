'''
Sensehat Dashboard
=========================================
Author: drdynscript
Modified: 03-12-2019
-----------------------------------------
Installation:
sudo pip install -U Flask (python2)
sudo pip3 install -U Flask (python3)
-----------------------------------------
Docs: http://flask.pocoo.org/docs/1.0/
=========================================
'''
# Import the libraries
from flask import Flask, jsonify, render_template, request
from sense_hat import SenseHat

# Variables
ambilight_obj = {
  'value': '#000000',
  'type': 'hex',
  'created': None
}

# Create an instance of flask
app = Flask(__name__)

# Create an instance of the sensehat
sense = SenseHat()

# Define the root route
@app.route('/')
def index():
  return 'Look the flask server is running'

# Define the nmd route
@app.route('/nmd')
def nmd():
  return 'Greetings Earthlings. We are NMDrs'

# Define the my_ip route
@app.route('/my_ip', methods=['GET'])
def my_ip():
  return jsonify({
    'ip': request.remote_addr
  }), 200

# Define the api_environment route
@app.route('/api/environment', methods=['GET'])
def api_environment():
  environment_obj = create_environment_object()
  return jsonify(environment_obj), 200

# Define the api_environment route
@app.route('/environment', methods=['GET'])
def environment():
  environment_obj = create_environment_object()
  return render_template('environment.html', environment=environment_obj)

# Define the ambilight route
@app.route('/ambilight', methods=['GET', 'POST'])
def ambilight():
  global ambilight_obj
  if(request.method == 'POST'):
    print(request.form['txtColor'])
    ambilight_obj['value'] = request.form['txtColor']    
  return render_template('ambilight.html', ambilight=ambilight_obj)

# Define the api_ambilight route
@app.route('/api/ambilight', methods=['GET', 'PUT'])
def api_ambilight():
  global ambilight_obj
  if(request.method == 'GET'):
    return jsonify(ambilight_obj), 200
  elif request.method == 'PUT':
    return jsonify(ambilight_obj), 200

# Create Environment object (json)
def create_environment_object():
  environment_obj = {
    'temperature': {
      'value': round(sense.get_temperature()),
      'unit': u'°C'
    },
    'humidity': {
      'value': round(sense.get_humidity()),
      'unit': u'%'
    },
    'pressure': {
      'value': round(sense.get_pressure()),
      'unit': u'mbar'
    }
  }
  return environment_obj

# Constants
host = '192.168.0.8'
port = 8080
# Main method for Flask server
if __name__ == '__main__':
  app.run(host = host, port = port, debug = True)