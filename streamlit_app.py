import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os

# --- 1. CONFIGURATION DE LA PAGE & STYLE (Bleu, Blanc, Noir) ---
st.set_page_config(
    page_title="Lemuria - Hub IA Madagascar",
    page_icon="🚀",
    layout="wide"
)

# CSS Personnalisé Moderne & Épuré
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #0F172A; }
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
    
    .stButton>button {
        background-color: #0052FF !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    .card {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        background-color: #F8F9FA;
        margin-bottom: 12px;
    }
    .badge-promo {
        background-color: #0052FF;
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CONNEXION SÉCURISÉE À TON PROJET GOOGLE AI STUDIO ---
API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
ADMIN_EMAIL = st.secrets.get("ADMIN_EMAIL", "votre-email@gmail.com")

if not API_KEY:
    st.error("⚠️ Clé API Google AI Studio introuvable. Ajoutez-la dans les Secrets Streamlit.")
    st.stop()

# Initialisation du client avec ta clé AI Studio
client = genai.Client(api_key=API_KEY)

# Session State pour les Analytics Backend
if "stats" not in st.session_state:
    st.session_state.stats = {"storyboards": 0, "prompts": 0, "clics_affiliations": 0}

if "code_promo" not in st.session_state:
    st.session_state.code_promo = "LEMURIA2026"

# SYSTEM INSTRUCTION (Mise en mémoire du comportement défini sur AI Studio)
SYSTEM_INSTRUCTIONS = """
Tu es "Lemuria", l'assistant virtuel intelligent du Hub IA de Madagascar.
Ton rôle est d'aider les créateurs à générer des storyboards pour Google Flow Beta et d'extraire des prompts précis à partir d'images pour PikverseAI.

Directives :
- Pour un Storyboard : Analyse l'image et génère un découpage en 3 à 5 scènes avec un prompt détaillé en anglais pour Google Flow.
- Pour une conversion Image -> Prompt : Donne un Prompt Master ultra-précis en anglais pour Pikverse / Midjourney.
- Intègre régulièrement des salutations chaleureuses en Malagasy.
"""

# --- 3. EN-TÊTE ET AUTHENTIFICATION GOOGLE ---
col_logo, col_auth = st.columns([3, 1])
with col_logo:
    st.title("🚀 LEMURIA")
    st.caption("Le Hub IA 100% gratuit de Madagascar • Google Flow Beta • PikverseAI")

with col_auth:
    user_email_input = st.text_input("Accès Admin / Google", placeholder="votre-email@gmail.com")

# MODULE D'ADMINISTRATION
is_admin = (user_email_input.strip().lower() == ADMIN_EMAIL.strip().lower())
if is_admin:
    st.success("🔓 Mode Admin Actif")
    with st.expander("📊 Analytics & Configuration Backend"):
        st.write("### Statistiques d'utilisation (Backend)")
        st.json(st.session_state.stats)
        
        st.write("### Modifier le Code Promo du Mois")
        nouveau_code = st.text_input("Nouveau Code :", value=st.session_state.code_promo)
        if st.button("Enregistrer"):
            st.session_state.code_promo = nouveau_code
            st.toast("Code promo mis à jour !")

st.divider()

# --- 4. CARROUSEL DES RÉSEAUX SOCIAUX (5 Slides) ---
st.subheader("🌐 Rejoignez la communauté Lemuria")
cols_rs = st.columns(5)

socials = [
    {"name": "Facebook", "url": "https://facebook.com", "icon": "📘"},
    {"name": "TikTok", "url": "https://tiktok.com", "icon": "🎵"},
    {"name": "YouTube", "url": "https://youtube.com", "icon": "🔴"},
    {"name": "Instagram", "url": "https://instagram.com", "icon": "📸"},
    {"name": "Telegram VIP", "url": "https://t.me", "icon": "✈️"}
]

for idx, col in enumerate(cols_rs):
    s = socials[idx]
    with col:
        if st.button(f"{s['icon']} {s['name']}", key=f"rs_{idx}"):
            st.session_state.stats["clics_affiliations"] += 1
            st.markdown(f"[Accéder à {s['name']}]({s['url']})")

st.divider()

# --- 5. INTERFACE INTERACTIVE (Appels à AI Studio) ---
st.subheader("🛠️ Outils de Création Visuelle")

tab1, tab2, tab3 = st.tabs(["🎬 Générateur Storyboard", "🎨 Image vers Prompt", "🛒 Boutique & Code Promo"])

# TAB 1 : GENERATEUR STORYBOARD FOR GOOGLE FLOW
with tab1:
    st.write("Importez une image pour générer votre storyboard prêt à coller dans **Google Flow Beta**.")
    img_file = st.file_uploader("Image de référence", type=["jpg", "jpeg", "png"], key="sb_img")
    
    if img_file and st.button("Générer avec Google AI Studio"):
        st.session_state.stats["storyboards"] += 1
        image = Image.open(img_file)
        st.image(image, caption="Image source", width=300)
        
        with st.spinner("Traitement par le modèle Gemini..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[image, "Crée un storyboard vidéo complet à partir de cette image pour Google Flow."],
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS)
            )
            st.markdown("### 📋 Storyboard prêt à être copié :")
            st.write(response.text)
            
            st.markdown("""
            <div class="card">
                👉 <b>Accéder directement à l'outil :</b> 
                <a href="https://google.com" target="_blank" style="color:#0052FF; font-weight:bold;">Ouvrir Google Flow Beta (Lien Partenaire Lemuria)</a>
            </div>
            """, unsafe_allow_html=True)

# TAB 2 : TRANSFORMATEUR IMAGE TO PROMPT
with tab2:
    st.write("Transformez n'importe quelle image en un Prompt Master pour **PikverseAI**.")
    img_prompt_file = st.file_uploader("Image d'inspiration", type=["jpg", "jpeg", "png"], key="p_img")
    
    if img_prompt_file and st.button("Extraire le Prompt Master"):
        st.session_state.stats["prompts"] += 1
        image = Image.open(img_prompt_file)
        
        with st.spinner("Analyse du style visuel..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[image, "Extrais le prompt anglais exact et détaillé pour reproduire cette image sur PikverseAI."],
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS)
            )
            st.code(response.text, language="markdown")
            st.info("👉 Copiez ce prompt et testez-le directement sur PikverseAI !")

# TAB 3 : BOUTIQUE & PROMO
with tab3:
    col_boutique, col_promo = st.columns(2)
    
    with col_boutique:
        st.write("### 🛒 Packs & Formations")
        st.markdown("""
        * **Pack Visuels E-Commerce Mada** (Inclus)
        * **Pack Prompts Réseaux Sociaux** (Inclus)
        * **Bundle Storyboard & Cinéma IA**
        """)
        
    with col_promo:
        st.write("### 🏷️ Code Promo du Mois")
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <h2>Code : <span class="badge-promo">{st.session_state.code_promo}</span></h2>
            <p>Donne accès à -50% sur nos offres partenaires et l'accès au groupe Telegram VIP Lemuria.</p>
        </div>
        """, unsafe_allow_html=True)
