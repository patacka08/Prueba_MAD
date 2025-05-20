import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import re

st.title("Procesador de archivos Excel")
uploaded_files = st.file_uploader("Subir archivos Excel", type=['xls','xlsx'], accept_multiple_files=True)
if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file)  # Leer cada Excel
        # (Lógica de extracción de nombre y agregar columnas igual que en paso previo)
        # ... (como se mostró arriba) ...
        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)  # Unir datos:contentReference[oaicite:11]{index=11}
    # Asignar Numero_ID único
    final_df['Numero_ID'] = pd.factorize(final_df['numero_documento'])[0] + 1  # (v. factorize:contentReference[oaicite:12]{index=12})
    # Reordenar columnas según necesidad (como arriba)
    # Mostrar tabla en la app
    st.dataframe(final_df)
    # Preparar y descargar Excel resultante
    def df_to_excel_bytes(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        return output.getvalue()
    excel_data = df_to_excel_bytes(final_df)
    st.download_button("Descargar resultado Excel", data=excel_data, file_name="resultado.xlsx")
