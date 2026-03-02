import streamlit as st
import requests
import base64
import os

# ==========================
# CONFIGURATION
# ==========================
st.set_page_config(page_title="M-IMMO LA REFERENCE", page_icon="🏠", layout="wide")

API_URL = "http://127.0.0.1:8000/api/"
ADMIN_EMAIL = "andremessing4@gmail.com"
ADMIN_PASSWORD = "admin@2026"
PAYMENT_NUMBER = "656770340"

# ==========================
# BACKGROUND
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
# SESSION
# ==========================
if "role" not in st.session_state:
    st.session_state.role = None

if "email" not in st.session_state:
    st.session_state.email = None

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

# ==========================
# SERVICES
# ==========================
st.markdown("## 🌟 Nos Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏘️ Location Sans Intermédiaire")

with col2:
    st.markdown("### 🔐 Sécurité")

with col3:
    st.markdown("### 💳 Paiement Mobile Money")
    st.write(f"Numéro : **{PAYMENT_NUMBER}**")

st.markdown("---")

# ==========================
# BOUTONS
# ==========================
col1, col2 = st.columns(2)

with col1:
    login_btn = st.button("🔐 Connexion")

with col2:
    signup_btn = st.button("📝 Inscription")

# ==========================
# CONNEXION
# ==========================
if login_btn:

    st.subheader("Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        try:
            # ADMIN LOCAL
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                st.session_state.role = "Admin"
                st.rerun()

            response = requests.post(
                API_URL + "login/",
                json={
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            data = response.json()

            if response.status_code == 200:
                st.session_state.role = data["role"]
                st.session_state.email = email
                st.success("Connexion réussie")
                st.rerun()
            else:
                st.error(data.get("error", "Erreur de connexion"))

        except requests.exceptions.RequestException:
            st.error("Impossible de contacter le serveur Django.")

# ==========================
# INSCRIPTION
# ==========================
if signup_btn:

    st.subheader("Créer un compte")

    nom = st.text_input("Nom")
    ville = st.text_input("Ville")
    telephone = st.text_input("Téléphone")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    role = st.selectbox("Type", ["Visiteur", "Proprietaire"])

    st.info(f"Paiement requis : 1000 FCFA au {PAYMENT_NUMBER}")

    transaction_id = st.text_input("Numéro de transaction")

    if st.button("Soumettre"):

        try:
            response = requests.post(
                API_URL + "register/",
                json={
                    "nom": nom,
                    "ville": ville,
                    "telephone": telephone,
                    "email": email,
                    "password": password,
                    "role": role,
                    "transaction_id": transaction_id
                },
                timeout=10
            )

            data = response.json()

            if response.status_code == 201:
                st.success("Compte créé avec succès")
            else:
                st.error(data.get("error", "Erreur d'inscription"))

        except requests.exceptions.RequestException:
            st.error("Impossible de contacter le serveur Django.")