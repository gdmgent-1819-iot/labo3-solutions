'''
Start to Code
=============
Workshop: Internet of Things (IoT)
Application: Ambilight
--------------------------------------
Author: Philippe De Pauw - Waterschoot
Opleiding: Grafische en digitale media
Specialisatie: New Media Development
'''

# Import the necessary libraries
from sense_hat import SenseHat
from time import sleep
import sys
import os
from google.cloud import firestore

# Constants
COLLECTION_NAME = u'pis'
PI_ID = u'stc_pi_1'

# Make an instance of SenseHat
sense = SenseHat()
sense.set_imu_config(False, False, False)
# Clear the RGB matrix
sense.clear()

# Initalize Firebase
# Use the service account for own server
os.chdir(os.path.dirname(__file__))
dirpath = os.getcwd()
db = firestore.Client.from_service_account_json(dirpath + '/config/start-to-code-70340204ea7b.json')

# function: on_snapshot(doc_snapshot, changes, read_time)
def convertHexValueToTuple(hex_value):
    r = int(hex_value[1:3], 16)
    g = int(hex_value[3:5], 16)
    b = int(hex_value[5:], 16)
    return (r, g, b)

# function: on_snapshot(doc_snapshot, changes, read_time)
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        doc_dict = doc.to_dict()
        print(doc_dict)
        if doc_dict['ambilight']['isOn'] == True:
            if doc_dict['ambilight']['color']['type'] == 'hex':
              color = convertHexValueToTuple(doc_dict['ambilight']['color']['value'])
            else:
              color = (0, 0, 255)
            sense.clear(color)
        else:
            sense.clear()

# Get the pi ref
pi_ref = db.collection(COLLECTION_NAME).document(PI_ID)
pi_watch = pi_ref.on_snapshot(on_snapshot)

while True:
    try:
        pass

    except (KeyboardInterrupt, SystemExit):
        print('Interrupt received! Stopping the application...')
        sense.clear()
        sys.exit(0)