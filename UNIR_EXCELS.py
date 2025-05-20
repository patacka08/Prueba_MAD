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
        # Obtener el nombre del archivo
        filename = uploaded_file.name  # Ejemplo: "Minera Centinela6010174087_5.xls"

        # Usar regex para extraer empresa y número de documento
        match = re.match(r"^(.*?)(\d{7,10})", filename)
        if match:
            empresa = match.group(1).strip()
            numero_documento = match.group(2)
        else:
            empresa = "Desconocida"
            numero_documento = "0000000000"
            st.warning(f"No se pudo extraer empresa y número del archivo: {filename}")

        try:
            # Leer hoja específica
            df = pd.read_excel(uploaded_file, sheet_name="Otro contenido")
            
            # Agregar columnas al DataFrame
            df["empresa"] = empresa
            df["numero_documento"] = numero_documento

            dfs.append(df)
        except ValueError:
            st.error(f"El archivo '{filename}' no contiene una hoja llamada 'Otro contenido'. Se omitirá.")

    if dfs:
        # Unir todos los DataFrames
        final_df = pd.concat(dfs, ignore_index=True)

        # Asignar Numero_ID único según numero_documento
        final_df['Numero_ID'] = pd.factorize(final_df['numero_documento'])[0] + 1

        # Reordenar columnas
        cols = final_df.columns.tolist()
        ordered_cols = ['Numero_ID', 'numero_documento', 'empresa'] + [col for col in cols if col not in ['Numero_ID', 'numero_documento', 'empresa']]
        final_df = final_df[ordered_cols]


        # Mostrar tabla en la app
        st.dataframe(final_df)

        # Preparar y descargar Excel resultante
        def df_to_excel_bytes(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.close()
            return output.getvalue()

        excel_data = df_to_excel_bytes(final_df)
        st.download_button("Descargar resultado Excel", data=excel_data, file_name="resultado.xlsx")
    else:
        st.warning("Ningún archivo válido fue procesado.")
