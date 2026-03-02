import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ==============================
# CONFIGURATION
# ==============================
st.set_page_config(page_title="Dashboard Admin", layout="wide")

# ==============================
# PROTECTION
# ==============================
if "role" not in st.session_state or st.session_state.role != "Admin":
    st.warning("Accès refusé.")
    st.stop()

# ==============================
# FICHIERS
# ==============================
USERS_FILE = "users.json"
ANNONCES_FILE = "annonces.json"

# ==============================
# FONCTIONS
# ==============================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def load_annonces():
    if os.path.exists(ANNONCES_FILE):
        with open(ANNONCES_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

def save_annonces(data):
    with open(ANNONCES_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)

# ==============================
# CHARGEMENT
# ==============================
users = load_users()
annonces = load_annonces()

# ==============================
# EXPIRATION AUTOMATIQUE
# ==============================
for email, user in users.items():

    if user.get("subscription_expiry"):

        expiry = datetime.fromisoformat(user["subscription_expiry"])

        if datetime.now() > expiry:

            user["approved"] = False
            user["payment_status"] = "expired"

save_users(users)

# ==============================
# NOTIFICATION PAIEMENT
# ==============================
pending_payments = [
    u for u in users.values()
    if u.get("payment_status") == "pending"
]

if len(pending_payments) > 0:
    st.success(f"🔔 {len(pending_payments)} paiement(s) en attente.")

# ==============================
# TITRE
# ==============================
st.title("📊 Dashboard Administrateur")

# ==============================
# STATISTIQUES
# ==============================
total_users = len(users)
total_annonces = len(annonces)

proprietaires = [u for u in users.values() if u["type"] == "Propriétaire"]
total_proprietaires = len(proprietaires)

revenu_estime = total_proprietaires * 1000

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Utilisateurs", total_users)
col2.metric("🏘️ Annonces", total_annonces)
col3.metric("🏢 Propriétaires", total_proprietaires)
col4.metric("💰 Revenu estimé", revenu_estime)

st.markdown("---")

# ==============================
# PAIEMENTS EN ATTENTE
# ==============================
st.subheader("💳 Paiements en attente")

for email, user in users.items():

    if user.get("payment_status") == "pending":

        st.markdown(f"""
        📧 **{email}**  
        👤 Nom: {user['nom']}  
        📱 Téléphone: {user['telephone']}  
        🧾 Transaction: {user['transaction_id']}
        """)

        if st.button("✔ Confirmer Paiement", key=f"pay_{email}"):

            users[email]["payment_status"] = "validated"
            users[email]["approved"] = True
            users[email]["subscription_expiry"] = (
                datetime.now() + timedelta(days=30)
            ).isoformat()

            save_users(users)
            st.success("Compte activé.")
            st.rerun()

        st.markdown("---")

# ==============================
# VALIDATION DES COMPTES
# ==============================
st.subheader("🔐 Comptes en attente")

for email, data in users.items():

    if not data.get("approved", False):

        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"📧 {email} — {data['type']}")

        with col2:
            if st.button("✔ Valider", key=f"val_{email}"):
                users[email]["approved"] = True
                save_users(users)
                st.rerun()

st.markdown("---")

# ==============================
# ANNONCES
# ==============================
st.subheader("🏘️ Toutes les annonces")

if not annonces:
    st.info("Aucune annonce.")
else:
    for annonce in annonces:

        st.markdown(f"""
        ### {annonce['type']} - {annonce['quartier']}
        **Prix :** {annonce['prix']} FCFA  
        **Propriétaire :** {annonce['proprietaire']}  
        **Contact :** {annonce['contact']}
        """)

        if annonce["photos"]:
            cols = st.columns(3)
            for i, path in enumerate(annonce["photos"]):
                with cols[i % 3]:
                    if os.path.exists(path):
                        st.image(path, use_container_width=True)

        if st.button("🗑 Supprimer", key=f"del_{annonce['id']}"):
            annonces.remove(annonce)
            save_annonces(annonces)
            st.rerun()

        st.markdown("---")

# ==============================
# DÉCONNEXION
# ==============================
if st.button("🚪 Déconnexion"):
    st.session_state.role = None
    st.session_state.email = None
    st.switch_page("app.py")