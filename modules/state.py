import streamlit as st

def init_session_state():
    """Initialise l'ensemble des variables globales dans st.session_state."""
    
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "Sombre Nuit"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "direct_agenda" not in st.session_state:
        st.session_state.direct_agenda = False

    if "agenda_active_tab" not in st.session_state:
        st.session_state.agenda_active_tab = "vue"

    if "agenda_events" not in st.session_state:
        st.session_state.agenda_events = []

    if "saved_prompts_library" not in st.session_state:
        st.session_state.saved_prompts_library = [
            {
                "title": "Flyer Événement Afro/DJ Ultra Réaliste",
                "category": "🎨 Génération d'images (Midjourney, DALL-E, Flux)",
                "prompt": "High-energy promotional flyer for an Afro-Fusion DJ event, neon magenta and deep violet lighting, gold accents, professional typography, cinematic atmosphere, 8k resolution, photorealistic, octane render --ar 4:5"
            },
            {
                "title": "Inpainting - Modification de fond de flyer",
                "category": "✏️ Modification & Retouche d'images",
                "prompt": "Isolate subject, replace background with a dark futuristic DJ booth filled with glowing purple lasers and subtle smoke machine haze, smooth blending"
            },
            {
                "title": "Refactoring Application Python Streamlit",
                "category": "🤖 Développement & Code AI",
                "prompt": "Refactor the following Python Streamlit code to use a modular architecture with separate views, clean session state initialization, and CSS Grid layout for responsiveness."
            },
            {
                "title": "Chanson Afrobeat / Bikutsi Anniversaire",
                "category": "🎵 Création Musicale & Paroles (Suno, Udio)",
                "prompt": "[Style: Afrobeat, Bikutsi, Uptempo 120 BPM, Energetic Brass, Lead Guitar, Cheerful Choirs]\n[Verse 1]\nAujourd'hui c'est la fête, on célèbre avec joie,\nLa famille rassemblée, pour chanter avec toi...\n[Chorus]\nJoyeux anniversaire, santé et bonheur !"
            }
        ]

    if "saved_code_snippets" not in st.session_state:
        st.session_state.saved_code_snippets = []

    if "saved_ideas" not in st.session_state:
        st.session_state.saved_ideas = []

    if "saved_current_projects" not in st.session_state:
        st.session_state.saved_current_projects = []

    if "saved_future_projects" not in st.session_state:
        st.session_state.saved_future_projects = []

    if "saved_links" not in st.session_state:
        st.session_state.saved_links = []

    if "saved_media_files" not in st.session_state:
        st.session_state.saved_media_files = []

    if "saved_api_keys" not in st.session_state:
        st.session_state.saved_api_keys = []

    if "saved_user_credentials" not in st.session_state:
        st.session_state.saved_user_credentials = []

    if "saved_contacts" not in st.session_state:
        st.session_state.saved_contacts = []

    if "saved_email_templates" not in st.session_state:
        st.session_state.saved_email_templates = []

    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"
