import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

def mostrar_mapa_dibujable(coordenadas):
    lat = coordenadas[0]
    lon = coordenadas[1]
    
    m = folium.Map(location=coordenadas, zoom_start=13, tiles="OpenStreetMap")

    rombo_coords = [
        [lat + 0.001, lon],
        [lat, lon + 0.001],
        [lat - 0.001, lon],
        [lat, lon - 0.001],
        [lat + 0.001, lon]
    ]
    folium.Polygon(
        locations=rombo_coords,
        color="green",
        fill=True,
        fill_color="lightgreen",
        fill_opacity=0.5,
        popup="Rombo automático"
    ).add_to(m)

    linea_coords = [[lat, lon], [lat - 0.0015, lon]]
    folium.PolyLine(locations=linea_coords, color="blue", weight=3).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup="📍 Punto de interés",
        icon=folium.Icon(color="red", icon="info-sign")
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
