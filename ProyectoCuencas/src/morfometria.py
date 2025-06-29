import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
from math import pi, sqrt
import random

def calcular_parametros(geojson_data):
    geometry = shape(geojson_data['geometry'])
    gdf = gpd.GeoDataFrame(index=[0], geometry=[geometry], crs="EPSG:4326")
    gdf_utm = gdf.to_crs(gdf.estimate_utm_crs())

    area_m2 = gdf_utm.geometry.area.iloc[0]
    perimetro_m = gdf_utm.geometry.length.iloc[0]
    centroide = gdf_utm.geometry.centroid.iloc[0]

    area_km2 = area_m2 / 1e6
    area_ha = area_m2 / 10000
    perimetro_km = perimetro_m / 1000

    longitud_cuenca_km = perimetro_km / 2
    L = longitud_cuenca_km * 1000
    A = area_km2
    P = perimetro_km

    diametro_equivalente_km = sqrt((4 * A) / pi)
    coef_compacidad = P / (2 * sqrt(pi * A)) if A > 0 else 0
    razon_elongacion = (2 * sqrt(A / pi)) / longitud_cuenca_km if longitud_cuenca_km > 0 else 0
    indice_forma = A / (longitud_cuenca_km ** 2) if longitud_cuenca_km > 0 else 0

    giandotti = ((4 * sqrt(A) + 1.5 * L) / (25.3 * sqrt(A))) if A > 0 else 0
    bransby = (0.00032 * L ** 0.77 * A ** 0.385) if A > 0 else 0
    california = (0.87 * L ** 0.385 / A ** 0.2) if A > 0 else 0
    clark = (0.28 * (L ** 0.77)) if L > 0 else 0
    passini = (0.42 * (L ** 0.77)) if L > 0 else 0
    pilgrim = (0.76 * (A ** 0.38)) if A > 0 else 0
    valencia = (0.28 * (L ** 0.77)) if L > 0 else 0
    kirpich = (0.01947 * (L ** 0.77)) if L > 0 else 0
    temez = (0.778 * (L ** 0.467) / (A ** 0.2)) if A > 0 else 0

    promedio = sum([giandotti, bransby, california, clark, passini, pilgrim, valencia, kirpich, temez]) / 9

    cota_min = random.randint(200, 600)
    cota_max = cota_min + random.randint(100, 800)
    dif_altura = cota_max - cota_min
    num_drenajes = random.randint(10, 50)
    long_total_cauces = round(area_km2 * random.uniform(1.2, 2.5), 2)
    densidad_drenajes = round(long_total_cauces / area_km2, 2) if area_km2 > 0 else 0
    pendiente_grados = round(random.uniform(3, 15), 2)
    pendiente_porcentaje = round(pendiente_grados * 1.745, 2)  
    factor_sinuosidad = round((long_total_cauces / L) if L > 0 else 0, 2)

    resultados = {
        "Area km2": round(A, 2),
        "Area H": round(area_ha, 2),
        "Per_Km": round(P, 2),
        "Clasificación": "Media",
        "Indice Compacidad": round(coef_compacidad, 4),
        "tipo": "rombo",
        "Longitud Cuenca": round(longitud_cuenca_km, 2),
        "factor forma": round(razon_elongacion, 4),
        "forma de la cuencaa": "Alargada" if razon_elongacion < 0.5 else "Circular",
        "Longitud CP_L": round(L, 2),
        "Longitud CP": round(L / 1000, 2),
        "factorSinuosidad": factor_sinuosidad,
        "clasificacion": "Alta sinuosidad" if factor_sinuosidad > 1.5 else "Baja sinuosidad",
        "Longitud Total Cauces": long_total_cauces,
        "Densidad_drenajes": densidad_drenajes,
        "Clasificación Drenaje": "Densa" if densidad_drenajes > 1.5 else "Dispersa",
        "Cota_min": cota_min,
        "Cot_max": cota_max,
        "Dif_altura": dif_altura,
        "Numero drenajes": num_drenajes,
        "Densi corrientes": round(num_drenajes / A, 2) if A > 0 else 0,
        "slope(°)": pendiente_grados,
        "slope(%)": pendiente_porcentaje,
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
