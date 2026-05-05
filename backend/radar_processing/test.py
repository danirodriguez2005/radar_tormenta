import requests
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

# 🌩️ Radar source (placeholder por ahora)
RADAR_URL = "https://www2.contingencias.mendoza.gov.ar/radar/sur.gif"  

# 🔐 Firebase init (desde GitHub Secrets)
cred_json = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)
db = firestore.client()

# 📥 Obtener último frame guardado
latest_query = (
    db.collection("radar_frames")
    .order_by("timestamp", direction=firestore.Query.DESCENDING)
    .limit(1)
    .stream()
)

latest_doc = None
for doc in latest_query:
    latest_doc = doc.to_dict()

# 🌩️ Descargar radar
response = requests.get(RADAR_URL)
timestamp = datetime.utcnow()

# 🧾 Nuevo documento
new_frame = {
    "timestamp": timestamp,
    "imageUrl": RADAR_URL,
    "status": "ok" if response.status_code == 200 else "error",
    "createdAt": "server"
}

# 🔁 lógica de deduplicación
should_save = True

if latest_doc:
    if latest_doc.get("imageUrl") == RADAR_URL:
        should_save = False

# 💾 guardar solo si hay cambios
if should_save:
    db.collection("radar_frames").add(new_frame)
    print("Frame guardado ✔️", timestamp)
else:
    print("Sin cambios, no se guarda 🚫", timestamp)

# 🧹 limpieza: mantener solo últimos 7 frames
all_docs = (
    db.collection("radar_frames")
    .order_by("timestamp", direction=firestore.Query.DESCENDING)
    .stream()
)

docs_list = list(all_docs)
MAX_FRAMES = 7

for doc in docs_list[MAX_FRAMES:]:
    doc.reference.delete()
