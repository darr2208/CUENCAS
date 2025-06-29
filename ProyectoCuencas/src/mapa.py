import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon

def mostrar_mapa_dibujable(coordenadas):
    lat, lon = coordenadas
    m = folium.Map(location=coordenadas, zoom_start=13, tiles="OpenStreetMap")

    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Watercolor').add_to(m)
    folium.TileLayer('CartoDB positron').add_to(m)
    folium.TileLayer('CartoDB dark_matter').add_to(m)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        name='Satélite'
    ).add_to(m)

    delta = 0.01
    rombo_coords = [
        [lat + delta, lon],
        [lat, lon + delta],
        [lat - delta, lon],
        [lat, lon - delta],
        [lat + delta, lon]
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

    folium.LayerControl().add_to(m)

    st_folium(m, width=900, height=600)

    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[ [c[1], c[0]] for c in rombo_coords ]]
        }
    }

