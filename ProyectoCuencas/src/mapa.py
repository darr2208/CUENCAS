import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

def mostrar_mapa_dibujable(coordenadas):
    m = folium.Map(location=coordenadas, zoom_start=14)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI Satellite',
        name='Satélite',
        overlay=False,
        control=True
    ).add_to(m)

    draw = Draw(
        export=False,
        draw_options={
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "circlemarker": False,
            "polygon": {
                "shapeOptions": {
                    "color": "#ff66cc",
                    "fillColor": "#ffe6f0",
                    "fillOpacity": 0.5
                }
            },
            "marker": True
        },
        edit_options={"edit": True}
    )
    draw.add_to(m)

    st_data = st_folium(m, width=900, height=600, returned_objects=["last_active_drawing"])

    if st_data and "last_active_drawing" in st_data and st_data["last_active_drawing"]:
        geometria = st_data["last_active_drawing"]["geometry"]
        tipo = geometria["type"]

        if tipo == "Polygon":
            coords = geometria["coordinates"][0]
            if len(coords) >= 4:
                lat = coords[0][1]
                lon = coords[0][0]
                folium.Marker(
                    location=[lat, lon],
                    popup="📍 Punto de interés (inicio del polígono)",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)
                st_folium(m, width=900, height=600)
            return {"tipo": "cuenca", "geojson": st_data["last_active_drawing"]}

        elif tipo == "Point":
            lat = geometria["coordinates"][1]
            lon = geometria["coordinates"][0]
            folium.Marker(
                location=[lat, lon],
                popup="📍 Punto de salida (desagüe)",
                icon=folium.Icon(color="blue", icon="tint")
            ).add_to(m)
            st_folium(m, width=900, height=600)
            return {"tipo": "punto_salida", "coordenadas": [lat, lon]}

    return None

