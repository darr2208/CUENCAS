import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from math import pi, sqrt

def calcular_parametros(geojson_data):
    geometry = shape(geojson_data['geometry'])
    gdf = gpd.GeoDataFrame(index=[0], geometry=[geometry], crs="EPSG:4326")
    gdf_utm = gdf.to_crs(gdf.estimate_utm_crs())

    area_m2 = gdf_utm.geometry.area.iloc[0]
    perimetro_m = gdf_utm.geometry.length.iloc[0]
    centroide = gdf_utm.geometry.centroid.iloc[0]

    area_km2 = area_m2 / 1e6
    perimetro_km = perimetro_m / 1000

    longitud_cuenca_km = perimetro_km / 2
    diametro_equivalente_km = sqrt((4 * area_km2) / pi)
    coef_compacidad = perimetro_km / (2 * sqrt(pi * area_km2)) if area_km2 > 0 else 0
    razon_elongacion = (2 * sqrt(area_km2 / pi)) / longitud_cuenca_km if longitud_cuenca_km > 0 else 0
    indice_forma = area_km2 / (longitud_cuenca_km ** 2) if longitud_cuenca_km > 0 else 0

    L = longitud_cuenca_km * 1000  # m
    A = area_km2
    P = perimetro_km

    giandotti = ((4 * sqrt(A) + 1.5 * L) / (25.3 * sqrt(A))) if A > 0 else 0
    bransby = (0.00032 * L ** 0.77 * A ** 0.385) if A > 0 else 0
    california = (0.87 * L ** 0.385 / A ** 0.2) if A > 0 else 0
    clark = (0.28 * (L ** 0.77)) if L > 0 else 0
    passini = (0.42 * (L ** 0.77)) if L > 0 else 0
    pilgrim = (0.76 * (A ** 0.38)) if A > 0 else 0
    valencia = (0.28 * (L ** 0.77)) if L > 0 else 0
    kirpich = (0.01947 * (L ** 0.77)) if L > 0 else 0
    temez = (0.778 * (L ** 0.467) / (A ** 0.2)) if A > 0 else 0

    promedio = sum([giandotti, bransby, california, clark, passini,
                    pilgrim, valencia, kirpich, temez]) / 9

    resultados = {
        "Área (km²)": round(area_km2, 2),
        "Perímetro (km)": round(perimetro_km, 2),
        "Centroide X": round(centroide.x, 2),
        "Centroide Y": round(centroide.y, 2),
        "Longitud de cuenca (km)": round(longitud_cuenca_km, 2),
        "Diámetro equivalente (km)": round(diametro_equivalente_km, 2),
        "Coef. de Compacidad": round(coef_compacidad, 4),
        "Razón de Elongación": round(razon_elongacion, 4),
        "Índice de Forma": round(indice_forma, 6),

        "Giandotti (h)": round(giandotti, 2),
        "Bransby-Williams (h)": round(bransby, 2),
        "California Culvert Practice (h)": round(california, 2),
        "Clark (h)": round(clark, 2),
        "Passini (h)": round(passini, 2),
        "Pilgrim y McDermott (h)": round(pilgrim, 2),
        "Valencia y Zuluaga (h)": round(valencia, 2),
        "Kirpich (h)": round(kirpich, 2),
        "Temez (h)": round(temez, 2),
        "Promedio Tc (h)": round(promedio, 2)
    }

    return gdf, resultados
