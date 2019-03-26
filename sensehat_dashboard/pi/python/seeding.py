'''
Start to Code
=============
Workshop: Internet of Things (IoT)
Application: Environment Sensors
--------------------------------------
Author: Philippe De Pauw - Waterschoot
Opleiding: Grafische en digitale media
Specialisatie: New Media Development
'''

# Import the necessary libraries
from sense_hat import SenseHat
from time import sleep
from datetime import datetime
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

# Get the pi environment ref
pi_ref = db.collection(COLLECTION_NAME).document(PI_ID)

try:
    for i in range(10, 11):
        ambilightObj = {
            u'color': {
                u'value': 0,
                u'type': u'hex'
            },
            u'isOn': True,
            u'modifiedAt': round(datetime.utcnow().timestamp() * 1000)
        }
        environmentObj = {
            u'temperature': {
                u'value': 0,
                u'unit_code': u'°C',
                u'unit_text': u'Celsius'
            },
            u'humidity': {
                u'value': 0,
                u'unit_code': u'%rH',
                u'unit_text': u'Percentage Relative Humidity'
            },
            u'pressure': {
                u'value': 0,
                u'unit_code': u'mbar',
                u'unit_text': u'Millibar'
            },
            u'modifiedAt': round(datetime.utcnow().timestamp() * 1000)
        }
        db.collection(COLLECTION_NAME).document('stc_pi_%s' % (i)).set({ 'ambilight': ambilightObj, 'environment': environmentObj })

except (KeyboardInterrupt, SystemExit):
        print('Interrupt received! Stopping the application...')
        sense.clear()
        sys.exit(0)