import streamlit as st

from app import paraphrase

st.set_page_config(page_title="Parafraseador IA", page_icon="📖", layout="wide")

st.markdown("""
<style>
.stApp { background: #efe8dc; }
.book-title { text-align:center; color:#3b2b20; font-family: Georgia, serif; font-size: 2.3rem; margin: .4rem 0 1.2rem; }
[data-testid="column"] { background:#fffdf7; border:1px solid #d8cbb7; border-radius:8px; padding:1.2rem; min-height:520px; box-shadow: 0 5px 18px #6f5b461c; }
textarea { font-family: Georgia, serif !important; font-size: 1.08rem !important; line-height: 1.65 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="book-title">📖 Parafraseador IA</div>', unsafe_allow_html=True)
left, right = st.columns(2, gap="large")

with left:
    st.subheader("Texto original")
    original = st.text_area("Escribe o pega aquí tu texto", height=390, key="original", label_visibility="collapsed")
    topic = st.text_input("Tema opcional para consultar Wikipedia", placeholder="Ej.: inteligencia artificial")
    provider = st.selectbox("Proveedor", ["auto", "ollama", "local", "nlpcloud", "huggingface", "iflytek"], index=0)
    model = st.text_input("Modelo Hugging Face", value="google/mt5-small")
    run = st.button("Parafrasear →", type="primary", use_container_width=True)

with right:
    st.subheader("Texto parafraseado")
    if run:
        if not original.strip():
            st.warning("Escribe primero el texto original.")
        else:
            with st.spinner("Reescribiendo..."):
                try:
                    result = paraphrase(original, topic or None, model or None, provider)
                    st.text_area("Resultado", value=result.text, height=390, label_visibility="collapsed")
                    st.caption(f"Proveedor utilizado: {result.source}")
                    if result.context:
                        with st.expander("Contexto de Wikipedia"):
                            st.write(result.context)
                except Exception as exc:
                    st.error(f"No se pudo generar el texto: {exc}")
    else:
        st.info("El texto parafraseado aparecerá aquí.")
