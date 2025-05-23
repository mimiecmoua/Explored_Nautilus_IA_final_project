#!/usr/bin/env python
# coding: utf-8

# In[14]:


import folium
from folium.plugins import MarkerCluster
import json
import pandas as pd
from math import radians, cos, sin, sqrt

# Chargement des données traduites / Loading translated data
with open('../notebooks/escales2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

def distance_from_center(lat):
    R = 6371e3  # rayon moyen en mètres / average radius in meters
    lat_rad = radians(lat)
    return sqrt((R * cos(lat_rad))**2 + (R * sin(lat_rad))**2)

df['Distance_Centre_Terre'] = df['Latitude_Décimal'].apply(distance_from_center).astype(int)

labels = {
    "fr": {
        "stop": "Escales du Nautilus",
        "date": "Date",
        "ocean": "Océan/Mer",
        "event": "Événement",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "distance": "Distance du centre de la Terre",
        "start": "Début",
        "end": "Fin",
        "start_popup": "Début du voyage",
        "end_popup": "Fin du voyage",
        "toggle_btn": "Fr / En"
    },
    "en": {
        "stop": "Nautilus Stops",
        "date": "Date",
        "ocean": "Ocean/Sea",
        "event": "Event",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "distance": "Distance from Earth's center",
        "start": "Start",
        "end": "End",
        "start_popup": "Start of the journey",
        "end_popup": "End of the journey",
        "toggle_btn": "Fr / En"
    }
}

# Fonction popup bilingue : français + anglais côte à côte, visibles simultanément / Bilingual pop-up function: French + English side by side, visible simultaneously
def make_bilingual_popup(row):
    fr = (
        f"🗺️🧭<b>{labels['fr']['stop']} :</b> {row['Escales du Nautilus']['fr']}<br>"
        f"📅 <b>{labels['fr']['date']} :</b> {row['Date']['fr']}<br>"
        f"🌊 <b>{labels['fr']['ocean']} :</b> {row['Océan/Mer']['fr']}<br>"
        f"📜 <b>{labels['fr']['event']} :</b> {row['Event']['fr']}<br>"
        f"↕️ <b>{labels['fr']['latitude']} :</b> {row['Latitude_Décimal']}<br>"
        f"↔️ <b>{labels['fr']['longitude']} :</b> {row['Longitude_Décimal']}<br>"
        f"🌍🧲 <b>{labels['fr']['distance']} :</b> {row['Distance_Centre_Terre']:,} mètres"
    )
    en = (
        f"🗺️🧭<b>{labels['en']['stop']} :</b> {row['Escales du Nautilus']['en']}<br>"
        f"📅 <b>{labels['en']['date']} :</b> {row['Date']['en']}<br>"
        f"🌊 <b>{labels['en']['ocean']} :</b> {row['Océan/Mer']['en']}<br>"
        f"📜 <b>{labels['en']['event']} :</b> {row['Event']['en']}<br>"
        f"↕️ <b>{labels['en']['latitude']} :</b> {row['Latitude_Décimal']}<br>"
        f"↔️ <b>{labels['en']['longitude']} :</b> {row['Longitude_Décimal']}<br>"
        f"🌍🧲 <b>{labels['en']['distance']} :</b> {row['Distance_Centre_Terre']:,} meters"
    )
    html = f"""
    <div style="display: flex; gap: 20px;">
        <div style="flex: 1; border-right: 1px solid #ccc; padding-right: 10px;">
            <h4>Français 🇫🇷</h4>
            {fr}
        </div>
        <div style="flex: 1; padding-left: 10px;">
            <h4>English 🇬🇧</h4>
            {en}
        </div>
    </div>
    """
    return html

# Création de la carte interactive du Nautilus IA embarquée / Creation of the interactive map of the Nautilus Onboard AI
m = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB positron')
cluster_layer = MarkerCluster().add_to(m)

coordinates = []
for _, row in df.iterrows():
    coord = [row['Latitude_Décimal'], row['Longitude_Décimal']]
    coordinates.append(coord)
    
    popup_html = make_bilingual_popup(row)
    folium.Marker(
        location=coord,
        popup=folium.Popup(popup_html, max_width=350),
        icon=folium.Icon(color='blue')
    ).add_to(cluster_layer)

folium.PolyLine(locations=coordinates, color='blue', weight=3, opacity=0.7).add_to(m)

# Marqueur début / Start marker
start_coord = coordinates[0]
folium.Marker(
    location=start_coord,
    popup=f"<div><b>{labels['fr']['start_popup']} / {labels['en']['start_popup']}</b></div>",
    icon=folium.DivIcon(
        icon_size=(30, 30),
        icon_anchor=(15, 15),
        html=f"<div style='font-size: 12px; color: green; font-weight: bold;'>{labels['fr']['start']} / {labels['en']['start']}</div>"
    )
).add_to(m)

# Marqueur fin / Fine marker
end_coord = coordinates[-1]
folium.Marker(
    location=end_coord,
    popup=f"<div><b>{labels['fr']['end_popup']} / {labels['en']['end_popup']}</b></div>",
    icon=folium.DivIcon(
        icon_size=(30, 30),
        icon_anchor=(15, 15),
        html=f"<div style='font-size: 12px; color: red; font-weight: bold;'>{labels['fr']['end']} / {labels['en']['end']}</div>"
    )
).add_to(m)

# Sauvegarde du fichier HTML / Saving the HTML file
output_file = r"C:\Users\Utilisateur\Documents\Nautilus_IA_Visualisation\notebooks\carte_nautilus_multilang.html"
m.save(output_file)



