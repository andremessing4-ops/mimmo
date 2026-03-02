import streamlit as st
import json
import os

# ==============================
# CONFIGURATION (DOIT ÊTRE EN PREMIER)
# ==============================
st.set_page_config(page_title="Espace Visiteur", layout="wide")

ANNONCES_FILE = "annonces.json"

# ==============================
# PROTECTION D'ACCÈS
# ==============================
if "role" not in st.session_state or st.session_state.role != "Visiteur":
    st.warning("Accès refusé. Veuillez vous connecter.")
    st.stop()

# ==============================
# FONCTION CHARGEMENT
# ==============================
def load_annonces():
    if os.path.exists(ANNONCES_FILE):
        with open(ANNONCES_FILE, "r") as f:
            return json.load(f)
    return []

annonces = load_annonces()

# ==============================
# INTERFACE
# ==============================
st.title("🏠 Chambres - Studios - Appartements disponibles")

if st.button("🚪 Déconnexion"):
    st.session_state.role = None
    st.session_state.email = None
    st.switch_page("app.py")

st.markdown("---")

# ==============================
# FILTRES
# ==============================
st.sidebar.header("🔎 Filtres")

quartiers = sorted(list(set([a["quartier"] for a in annonces if a["quartier"]])))
types = sorted(list(set([a["type"] for a in annonces])))

filtre_quartier = st.sidebar.selectbox("Quartier", ["Tous"] + quartiers)
filtre_type = st.sidebar.selectbox("Type de logement", ["Tous"] + types)

# ==============================
# APPLICATION DES FILTRES
# ==============================
annonces_filtrees = annonces

if filtre_quartier != "Tous":
    annonces_filtrees = [
        a for a in annonces_filtrees if a["quartier"] == filtre_quartier
    ]

if filtre_type != "Tous":
    annonces_filtrees = [
        a for a in annonces_filtrees if a["type"] == filtre_type
    ]

# ==============================
# AFFICHAGE
# ==============================
if not annonces_filtrees:
    st.info("Aucune annonce disponible pour le moment.")
else:
    for annonce in annonces_filtrees:

        st.markdown(f"""
        ### {annonce['type']} - {annonce['quartier']}
        **Prix :** {annonce['prix']} FCFA  
        **Contact :** {annonce['contact']}
        """)

        # Affichage photos sauvegardées
        if annonce["photos"]:
            cols = st.columns(3)
            for i, path in enumerate(annonce["photos"]):
                with cols[i % 3]:
                    st.image(path, use_container_width=True)

        # Bouton WhatsApp automatique
        whatsapp_number = annonce["contact"].replace(" ", "").replace("+", "")
        whatsapp_link = f"https://wa.me/{whatsapp_number}"

        st.markdown(
            f"[📞 Contacter sur WhatsApp]({whatsapp_link})",
            unsafe_allow_html=True
        )

        st.markdown("---")