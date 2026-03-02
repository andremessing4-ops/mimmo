import streamlit as st
import json
import os
import uuid

# ==============================
# CONFIGURATION
# ==============================
st.set_page_config(page_title="Espace Propriétaire", layout="wide")

ANNONCES_FILE = "annonces.json"
UPLOAD_FOLDER = "uploads"

# ==============================
# PROTECTION
# ==============================
if "role" not in st.session_state or st.session_state.role != "Propriétaire":
    st.warning("Accès refusé.")
    st.stop()

# ==============================
# FONCTIONS
# ==============================
def load_annonces():
    if os.path.exists(ANNONCES_FILE):
        with open(ANNONCES_FILE, "r") as f:
            return json.load(f)
    return []

def save_annonces(data):
    with open(ANNONCES_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Créer dossier uploads si inexistant
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# INITIALISATION
# ==============================
annonces = load_annonces()
email_proprietaire = st.session_state.email

st.title("🏢 Espace Propriétaire")
st.write(f"Bienvenue {email_proprietaire}")

if st.button("🚪 Déconnexion"):
    st.session_state.role = None
    st.session_state.email = None
    st.switch_page("app.py")

st.markdown("---")

# ==============================
# AJOUTER UN BIEN
# ==============================
st.subheader("➕ Ajouter un nouveau bien")

types_logement = [
    "Chambre simple",
    "Chambre moderne",
    "Studio simple",
    "Studio moderne",
    "Appartement"
]

type_bien = st.selectbox("Type de logement", types_logement)
quartier = st.text_input("Quartier")
prix = st.number_input("Prix (FCFA)", min_value=0)

contact = st.text_input("Votre numéro de contact")

photos = st.file_uploader(
    "Ajouter des photos",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if st.button("📢 Publier"):
    if not quartier or not contact:
        st.warning("Veuillez remplir tous les champs.")
    else:
        photo_paths = []

        for photo in photos:
            unique_name = f"{uuid.uuid4()}.jpg"
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)

            with open(file_path, "wb") as f:
                f.write(photo.read())

            photo_paths.append(file_path)

        nouvelle_annonce = {
            "id": str(uuid.uuid4()),
            "proprietaire": email_proprietaire,
            "type": type_bien,
            "quartier": quartier,
            "prix": prix,
            "contact": contact,
            "photos": photo_paths
        }

        annonces.append(nouvelle_annonce)
        save_annonces(annonces)

        st.success("Annonce publiée avec succès ✅")
        st.rerun()

st.markdown("---")

# ==============================
# MES ANNONCES (Filtrées)
# ==============================
st.subheader("📋 Mes annonces")

mes_annonces = [a for a in annonces if a["proprietaire"] == email_proprietaire]

if not mes_annonces:
    st.info("Vous n'avez aucune annonce.")

for annonce in mes_annonces:

    st.markdown(f"""
    ### {annonce['type']} - {annonce['quartier']}
    **Prix :** {annonce['prix']} FCFA  
    **Contact :** {annonce['contact']}
    """)

    # Affichage photos sauvegardées
    cols = st.columns(3)
    for i, path in enumerate(annonce["photos"]):
        with cols[i % 3]:
            st.image(path, use_container_width=True)

    col1, col2 = st.columns(2)

    # Supprimer
    with col1:
        if st.button("🗑 Supprimer", key=annonce["id"]):
            # Supprimer images du disque
            for path in annonce["photos"]:
                if os.path.exists(path):
                    os.remove(path)

            annonces.remove(annonce)
            save_annonces(annonces)
            st.success("Annonce supprimée.")
            st.rerun()

    st.markdown("---")