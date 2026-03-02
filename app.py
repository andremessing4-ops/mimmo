import streamlit as st
import hashlib
import json
import os
import base64
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
st.set_page_config(page_title="M-IMMO LA REFERENCE", page_icon="🏠", layout="wide")

# ==========================
# ARRIÈRE PLAN SOMBRE
# ==========================
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, p, label {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if os.path.exists("background.jpg"):
    set_background("background.jpg")

# ==========================
# ADMIN FIXE
# ==========================
ADMIN_EMAIL = "andremessing4@gmail.com"
ADMIN_PASSWORD = "admin@2026"
PAYMENT_NUMBER = "656770340"
FILE_NAME = "users.json"

# ==========================
# FONCTIONS
# ==========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(FILE_NAME, "w") as f:
        json.dump(users, f, indent=4, default=str)

# ==========================
# INITIALISATION SESSION
# ==========================
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "role" not in st.session_state:
    st.session_state.role = None

if "email" not in st.session_state:
    st.session_state.email = None

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ==========================
# REDIRECTION
# ==========================
if st.session_state.role == "Admin":
    st.switch_page("pages/3_Admin.py")

if st.session_state.role == "Visiteur":
    st.switch_page("pages/1_Visiteur.py")

if st.session_state.role == "Propriétaire":
    st.switch_page("pages/2_Proprietaire.py")

# ==========================
# TITRE
# ==========================
st.title("🏠 M-IMMO LA RÉFÉRENCE")
st.markdown("---")
st.markdown("createur : **Andre Messing** / contact : **656770340**")

# ==========================
# SERVICES
# ==========================
st.markdown("## 🌟 Nos Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏘️ Location Sans Intermédiaire")
    st.write("Chambres • Studios • Appartements • Maisons")

with col2:
    st.markdown("### 🔐 Sécurité et Fiabilité")
    st.write("✔️ Comptes validés ✔️ Protection ✔️ Gestion contrôlée")

with col3:
    st.markdown("### 💳 Paiement Mobile Money")
    st.write(f"📱 MTN / Orange Money\n💰 Numéro : **{PAYMENT_NUMBER}**")

st.markdown("---")

# ==========================
# BOUTONS
# ==========================
col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Connexion"):
        st.session_state.show_login = True
        st.session_state.show_signup = False

with col2:
    if st.button("📝 Inscription"):
        st.session_state.show_signup = True
        st.session_state.show_login = False

# ==========================
# MODAL CONNEXION
# ==========================
@st.dialog("Connexion")
def login_modal():

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            st.session_state.role = "Admin"
            st.session_state.show_login = False
            st.rerun()

        user = st.session_state.users.get(email)

        if not user:
            st.error("Compte introuvable.")

        elif user["password"] != hash_password(password):
            st.error("Mot de passe incorrect.")

        elif not user.get("approved", False):
            st.warning("Compte non validé.")

        else:
            st.session_state.role = user["type"]
            st.session_state.email = email
            st.session_state.show_login = False
            st.rerun()

    if st.button("Fermer"):
        st.session_state.show_login = False
        st.rerun()

# ==========================
# MODAL INSCRIPTION
# ==========================
@st.dialog("Créer un compte")
def signup_modal():

    nom = st.text_input("Nom")
    ville = st.text_input("Ville")
    telephone = st.text_input("Téléphone")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    account_type = st.selectbox("Type", ["Visiteur", "Propriétaire"])

    st.info(f"Envoyez 1000 FCFA au numéro : {PAYMENT_NUMBER} pour validation de votre compte et entrez le numero de transaction ci-dessous.")

    transaction_id = st.text_input("Numéro de transaction")

    if st.button("Soumettre"):

        if email == ADMIN_EMAIL:
            st.warning("Email réservé à l'admin.")

        elif email in st.session_state.users:
            st.warning("Email déjà utilisé.")

        elif not nom or not ville or not telephone or not transaction_id:
            st.warning("Remplir tous les champs.")

        else:
            st.session_state.users[email] = {
                "nom": nom,
                "ville": ville,
                "telephone": telephone,
                "password": hash_password(password),
                "type": account_type,
                "approved": False,
                "transaction_id": transaction_id,
                "payment_status": "pending",
                "subscription_expiry": None
            }

            save_users(st.session_state.users)

            st.success("Demande envoyée. En attente de validation.")
            st.session_state.show_signup = False
            st.rerun()

    if st.button("Fermer"):
        st.session_state.show_signup = False
        st.rerun()

# ==========================
# APPEL SECURISE
# ==========================
if st.session_state.show_login:
    login_modal()

if st.session_state.show_signup:
    signup_modal()