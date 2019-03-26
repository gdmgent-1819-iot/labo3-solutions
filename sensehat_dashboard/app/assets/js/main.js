/*
Start 2 Code
============
Workshop: Internet of Things
Application: Ambilight
Description: 
  - Change the RGBMatrix on the RaspberryPi via Firestore
  - Input-fields: color and switch
  - Listen to updates in the corresponding Firestore document (and update the UI)
Technology:
  - HTML
  - CSS
    - Libraries:
      - fontawesome
  - JavaScript
    - Libraries:
      - firebasejs
Cloud:
  - Firestore (Firebase)
*/

'use strict'

const config = {
  firebase: {
    apiKey: '',
    authDomain: '',
    databaseURL: '',
    projectId: '',
    storageBucket: '',
    messagingSenderId: '',
  },
  pis_collection_name: '',
  pi_id: '',
}

function convertTimeMillisToDate(millis) {
  const localOffsetDate = new Date().getTimezoneOffset()
  let realLocalDate = new Date(millis)
  realLocalDate.setHours(realLocalDate.getHours()-localOffsetDate/60)
  return realLocalDate.toLocaleString();
}

;((window) => {
  const app = {
    init() {
      // Initialize firebase
      firebase.initializeApp(config.firebase)
      // Initialize Cloud Firestore through Firebase
      this._firestore = firebase.firestore()
      // Disable deprecated features
      this._firestore.settings({
        timestampsInSnapshots: true
      })
      // Cache DOM-elements
      this.cacheDOMElements(); 

      // Get the ambilight via Firebase collection and document child
      this._piRef = this._firestore.collection(config.pis_collection_name).doc(config.pi_id);
      this._ambiLightData = {
        isOn: false,
        color: {
          value: '#000000',
          type: 'hex'
        }
      }
      this._environmentData = {
      }
      this._piRef.get().then((doc) => {
          if (doc.exists) {
            console.log(doc.data().ambilight)
            console.log(doc.data().environment)
            this._ambiLightData = doc.data().ambilight
            this._environmentData = doc.data().environment
            this._piRef.onSnapshot((doc) => {
              this._ambiLightData = doc.data().ambilight
              this._environmentData = doc.data().environment
              this.updateUI();
            })
          }
      }).catch((error) => {
          console.log("Error getting document:", error)
      })
    },
    cacheDOMElements() {
      // Environment DOM Elements
      this._$environment__modified_at = document.querySelector('#environment__modified_at')
      this._$environment__temperature = document.querySelector('#environment__temperature')
      this._$environment__humidity = document.querySelector('#environment__humidity')
      this._$environment__pressure = document.querySelector('#environment__pressure')

      // RGB Led Matrix
      this._$rgbmatrix = document.querySelector('#rgbmatrix')
      this._$rgbmatrixBulb = document.querySelector('.rgbmatrix__bulb')
      this._$chkRgbmatrixState = document.querySelector('#chkRgbmatrixState')
      if(this._$chkRgbmatrixState) {
        this._$chkRgbmatrixState.addEventListener('change', (ev) => {
          ev.preventDefault()
          this._ambiLightData.isOn = ev.target.checked
          this.updateAmbilightInFirebase()
          return false
        })
      }
      this._$txtRgbmatrixColor = document.querySelector('#txtRgbmatrixColor')
      this._picker = new CP(this._$txtRgbmatrixColor);
      this._picker.on('stop', (color) => {
          this._$txtRgbmatrixColor.value = '#' + color;
          this._ambiLightData.color.value = this._$txtRgbmatrixColor.value
          this._ambiLightData.color.type = 'hex'

          this.updateUI()
          this.updateAmbilightInFirebase()
      })
    },
    updateUI() {
      if(this._$rgbmatrix) {
        this._$rgbmatrix.style.background = this._ambiLightData.color.value
      }
      if(this._$rgbmatrixBulb) {
        this._$rgbmatrixBulb.style.color = this._ambiLightData.color.value
      }
      if(this._$txtRgbmatrixColor) {
        this._$txtRgbmatrixColor.value = this._ambiLightData.color.value;
      }
      if(this._$chkRgbmatrixState) {
        this._$chkRgbmatrixState.checked = this._ambiLightData.isOn;
      }

      // Environment
      if(this._$environment__modified_at) {
        this._$environment__modified_at.innerHTML = `<span class="value">${ convertTimeMillisToDate(this._environmentData.modifiedAt) }</span>`
      }
      if(this._$environment__temperature) {
        this._$environment__temperature.innerHTML = `<span class="value">${this._environmentData.temperature.value}</span><span class="label">${this._environmentData.temperature.unit_code} (${this._environmentData.temperature.unit_text})</span>`
      }
      if(this._$environment__humidity) {
        this._$environment__humidity.innerHTML = `<span class="value">${this._environmentData.humidity.value}</span><span class="label">${this._environmentData.humidity.unit_code} (${this._environmentData.humidity.unit_text})</span>`
      }
      if(this._$environment__pressure) {
        this._$environment__pressure.innerHTML = `<span class="value">${this._environmentData.pressure.value}</span><span class="label">${this._environmentData.pressure.unit_code} (${this._environmentData.pressure.unit_text})</span>`
      }
    },
    updateAmbilightInFirebase() {
      this._piRef.get().then((doc) => {
          if (doc.exists) {
              this._piRef.set({ ambilight: this._ambiLightData }, { merge: true }).then(() => {
                console.log('Document updated!')
              }).catch((error) => {
                console.log('Error writing document: ${error}')
              })
          } else {
              console.log("No such document!")
          }
      }).catch((error) => {
          console.log("Error getting document:", error)
      })
    }
  }

  // Initalize application
  app.init()
})(window)