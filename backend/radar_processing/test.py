import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

RADAR_URL = "https://www2.contingencias.mendoza.gov.ar/radar/sur.gif"  

cred_json = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()

# --- fetch radar ---
response = requests.get(RADAR_URL)

timestamp = datetime.utcnow()

doc = {
    "timestamp": timestamp,
    "imageUrl": RADAR_URL,
    "status": "ok" if response.status_code == 200 else "error",
    "httpStatus": response.status_code,
    "source": "radar_job"
}

db.collection("radar_frames").add(doc)

print("Frame guardado ✔️", timestamp)

