import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

RADAR_URL = "https://www2.contingencias.mendoza.gov.ar/radar/sur.gif"  

# --- Firebase init ---
cred_json = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Fetch radar ---
response = requests.get(RADAR_URL)

timestamp = datetime.utcnow().isoformat()

if response.status_code == 200:
    doc = {
        "timestamp": timestamp,
        "imageUrl": RADAR_URL,
        "status": "ok"
    }

    db.collection("radar_frames").add(doc)
    print("Metadata guardada ✔️", timestamp)
else:
    doc = {
        "timestamp": timestamp,
        "imageUrl": RADAR_URL,
        "status": "error",
        "httpStatus": response.status_code
    }

    db.collection("radar_frames").add(doc)
    print("Error guardado ✔️", response.status_code)
