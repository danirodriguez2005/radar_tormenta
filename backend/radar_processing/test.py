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

# --- Get latest frame ---
latest = db.collection("radar_frames") \
    .order_by("timestamp", direction=firestore.Query.DESCENDING) \
    .limit(1) \
    .stream()

latest_doc = None
for doc in latest:
    latest_doc = doc.to_dict()

# --- Fetch radar ---
response = requests.get(RADAR_URL)

timestamp = datetime.utcnow()

new_doc = {
    "timestamp": timestamp,
    "imageUrl": RADAR_URL,
    "status": "ok" if response.status_code == 200 else "error"
}

# --- Dedup logic ---
should_save = True

if latest_doc:
    if latest_doc.get("imageUrl") == RADAR_URL:
        should_save = False

# --- Save only if changed ---
if should_save:
    db.collection("radar_frames").add(new_doc)
    print("Frame guardado ✔️", timestamp)
else:
    print("Sin cambios, no se guarda 🚫")
