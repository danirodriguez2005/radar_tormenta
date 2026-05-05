import requests

RADAR_URL = "https://www2.contingencias.mendoza.gov.ar/radar/sur.gif"  

response = requests.get(RADAR_URL)

if response.status_code == 200:
    with open("radar.gif", "wb") as f:
        f.write(response.content)
    print("Radar descargado correctamente ✔️")
else:
    print("Error descargando radar:", response.status_code)
