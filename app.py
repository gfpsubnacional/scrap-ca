import streamlit as st
import requests
import pandas as pd

# Título de la página
st.title("Web Scraper de Consulta Amigable")

# Formulario para ingresar parámetros
gobierno_regional = st.text_input("Gobierno Regional", "Loreto")
categoria_presupuestal = st.text_input("Categoría Presupuestal", "57")

# Botón para ejecutar el scraping
if st.button("Scrapear"):
    with st.spinner("Ejecutando el scraping..."):
        # Hacer la solicitud POST a la API de Render
        try:
            response = requests.post(
                "https://scrap-ca.onrender.com/scrape",  # Sustituye con tu URL de Render
                json={"gobierno_regional": gobierno_regional, "categoria_presupuestal": categoria_presupuestal}
            )
            data = response.json()
            
            # Si la respuesta es exitosa, mostrar los resultados
            if data.get("status") == "success":
                st.success("Resultado del Scraping:")
                # Convierte el diccionario de vuelta a un DataFrame
                result_df = pd.DataFrame(data["data"])
                st.dataframe(result_df)
            else:
                st.error(f"Error: {data.get('message')}")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
