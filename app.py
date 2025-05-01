import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from collections import Counter
from googletrans import Translator

# -------------------- CONFIGURACIÓN GENERAL --------------------
st.set_page_config(page_title="📊 Analizador de Texto Inteligente", page_icon="🧠", layout="wide")

st.markdown("<h1 style='text-align: center;'>📝 Analizador de Texto con TextBlob</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-size: 16px;'>Analiza el sentimiento, subjetividad y frecuencia de palabras en tu texto</div>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- ENTRADA DE TEXTO --------------------
st.sidebar.header("⚙️ Opciones de Entrada")
modo = st.sidebar.radio("Selecciona el modo:", ["Texto directo", "Archivo .txt"])

texto_entrada = ""
if modo == "Texto directo":
    texto_entrada = st.text_area("✍️ Escribe o pega tu texto aquí:", height=200)
else:
    archivo = st.file_uploader("📂 Sube un archivo .txt", type="txt")
    if archivo is not None:
        texto_entrada = archivo.read().decode("utf-8")

# -------------------- ANÁLISIS --------------------
if texto_entrada:
    st.markdown("## 📋 Resultados del análisis")

    # Análisis con TextBlob
    blob = TextBlob(texto_entrada)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity

    # Frases traducidas
    traductor = Translator()
    frases = [str(oracion) for oracion in blob.sentences]
    frases_traducidas = []
    for frase in frases:
        try:
            traduccion = traductor.translate(frase, src='es', dest='en').text
            frases_traducidas.append((frase, traduccion))
        except:
            frases_traducidas.append((frase, "[Error al traducir]"))

    # Contador de palabras sin stopwords
    texto_limpio = re.sub(r"[^\w\s]", "", texto_entrada.lower())
    palabras = texto_limpio.split()
    STOP_WORDS = set([
        "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para",
        "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este",
        "sí", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "también", "me", "hasta",
        "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni",
        "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos",
        "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho",
        "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo",
        "nosotros", "mi", "mis", "tú", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosotros",
        "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas"
    ])
    palabras_filtradas = [p for p in palabras if p not in STOP_WORDS]
    contador = Counter(palabras_filtradas)
    top_palabras = contador.most_common(10)

    # -------------------- VISUALIZACIÓN --------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 Sentimiento")
        sentimiento_norm = (sentimiento + 1) / 2
        st.progress(sentimiento_norm)
        if sentimiento > 0.05:
            st.success(f"📈 Positivo ({sentimiento:.2f})")
        elif sentimiento < -0.05:
            st.error(f"📉 Negativo ({sentimiento:.2f})")
        else:
            st.info(f"📊 Neutral ({sentimiento:.2f})")

    with col2:
        st.markdown("### 🧠 Subjetividad")
        st.progress(subjetividad)
        st.write(f"Subjetividad: {subjetividad:.2f}")
        st.caption("0 es objetivo, 1 es totalmente subjetivo")

    st.markdown("---")

    st.markdown("## 🧾 Traducción de frases")
    for i, (frase, traduccion) in enumerate(frases_traducidas, 1):
        with st.expander(f"Frase {i}"):
            st.write(f"**Original:** {frase}")
            st.write(f"**Traducido:** {traduccion}")

    st.markdown("---")

    st.markdown("## 🔡 Palabras más frecuentes")
    if top_palabras:
        df = pd.DataFrame(top_palabras, columns=["Palabra", "Frecuencia"])
        st.bar_chart(df.set_index("Palabra"))
    else:
        st.info("No se encontraron palabras frecuentes.")
else:
    st.info("🕵️‍♀️ Ingresa un texto o sube un archivo para comenzar el análisis.")


