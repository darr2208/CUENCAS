import folium
from streamlit_folium import st_folium

def mostrar_mapa_dibujable(coordenadas):
    lat, lon = coordenadas
    m = folium.Map(location=coordenadas, zoom_start=13, tiles="OpenStreetMap")

    delta = 0.01  # puedes ajustar este valor para agrandar o reducir el rombo
    rombo_coords = [
        [lat + delta, lon],
        [lat, lon + delta],
        [lat - delta, lon],
        [lat, lon - delta],
        [lat + delta, lon]  # cerrar el polígono
    ]

    folium.Polygon(
        locations=rombo_coords,
        color="purple",
        fill=True,
        fill_color="#ffe6f0",
        fill_opacity=0.5,
        popup="Rombo generado automáticamente"
    ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup="📍 Punto de interés (centro del rombo)",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    st_folium(m, width=900, height=600)

    return {
        "tipo": "cuenca",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[ [c[1], c[0]] for c in rombo_coords ]]  # invertir lat-lon a lon-lat
        }
    }
