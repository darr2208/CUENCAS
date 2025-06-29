import io
import geopandas as gpd
import pandas as pd
import tempfile
import zipfile
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import BarChart, Reference

def exportar_shapefile_zip(gdf):
    with tempfile.TemporaryDirectory() as tmpdir:
        shp_path = os.path.join(tmpdir, "cuenca.shp")
        gdf.to_crs("EPSG:4326").to_file(shp_path, driver="ESRI Shapefile")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for ext in [".shp", ".shx", ".dbf", ".prj"]:
                file_path = os.path.join(tmpdir, f"cuenca{ext}")
                zipf.write(file_path, arcname=f"cuenca{ext}")
        zip_buffer.seek(0)
        return zip_buffer

def exportar_excel(resultados_dict):
    parametros_geom = {k: v for k, v in resultados_dict.items() if "h)" not in k}
    tiempos_conc = {k: v for k, v in resultados_dict.items() if "h)" in k}

    wb = Workbook()

    ws1 = wb.active
    ws1.title = "Parámetros Geométricos"
    df_geom = pd.DataFrame(parametros_geom.items(), columns=["Parámetro", "Valor"])
    ws1.append(['Parámetro', 'Valor'])
    for row in dataframe_to_rows(df_geom, index=False, header=False):
        ws1.append(row)

    ws2 = wb.create_sheet(title="Tiempos de Concentración")
    df_tc = pd.DataFrame(tiempos_conc.items(), columns=["Método", "Tiempo (h)"])
    ws2.append(['Método', 'Tiempo (h)'])
    for row in dataframe_to_rows(df_tc, index=False, header=False):
        ws2.append(row)

    last_row = ws2.max_row + 1
    ws2[f"A{last_row}"] = "Promedio Tc (h)"
    ws2[f"B{last_row}"] = f"=AVERAGE(B2:B{last_row - 1})"

    chart = BarChart()
    chart.title = "Comparativa de Métodos"
    chart.x_axis.title = "Método"
    chart.y_axis.title = "Tiempo (h)"
    chart.width = 20
    chart.height = 10

    data = Reference(ws2, min_col=2, min_row=2, max_row=last_row - 1)
    cats = Reference(ws2, min_col=1, min_row=2, max_row=last_row - 1)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)
    ws2.add_chart(chart, "E2")

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
