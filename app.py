# Visualización de sentimiento y subjetividad
def crear_visualizaciones(resultados):
    st.markdown("## 🎭 Análisis de Sentimiento y Subjetividad")
    st.markdown("Mira cómo se siente el texto ingresado según el análisis de TextBlob.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 Sentimiento")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")

    with col2:
        st.markdown("### 🧠 Subjetividad")
        st.progress(resultados["subjetividad"])
        st.write(f"**Subjetividad:** {resultados['subjetividad']:.2f}")
        st.caption("0 es objetivo, 1 es totalmente subjetivo")

    st.markdown("---")
    
    # Frases originales y traducidas
    st.markdown("## 🧾 Frases originales y traducidas")
    for i, frase in enumerate(resultados["frases"], 1):
        with st.expander(f"Frase {i}"):
            st.write(f"**Original:** {frase['original']}")
            st.write(f"**Traducido:** {frase['traducido']}")

    st.markdown("---")

    # Frecuencia de palabras
    st.markdown("## 🔤 Palabras más frecuentes")
    top_palabras = list(resultados["contador_palabras"].items())[:10]
    if top_palabras:
        df = pd.DataFrame(top_palabras, columns=["Palabra", "Frecuencia"])
        st.bar_chart(df.set_index("Palabra"))
    else:
        st.info("No se encontraron palabras significativas.")

