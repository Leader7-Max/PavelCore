import streamlit as st

def render_badge(text, variant="pink"):
    """Affiche un badge stylisé."""
    bg_color = "rgba(236, 72, 153, 0.1)" if variant == "pink" else "rgba(16, 185, 129, 0.1)"
    text_color = "#DB2777" if variant == "pink" else "#059669"
    border_color = "rgba(236, 72, 153, 0.2)" if variant == "pink" else "rgba(16, 185, 129, 0.2)"
    
    return f"""
        <span style="
            background: {bg_color};
            color: {text_color};
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid {border_color};
        ">{text}</span>
    """

def render_card(title, content_html, badge_text="", badge_variant="pink", border_color="#EC4899"):
    """Génère une carte standardisée pour PavelCore."""
    badge_html = render_badge(badge_text, badge_variant) if badge_text else ""
    
    card_html = f"""
        <div class="zapio-card" style="border-left: 5px solid {border_color};">
            {badge_html}
            <h4 style="margin-top: 8px; color: #FFF;">{title}</h4>
            <div style="margin-top: 6px; font-size: 0.9rem;">
                {content_html}
            </div>
        </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_section_header(title, subtitle="", badge=""):
    """Génère un en-texte de section propre et cohérent."""
    badge_html = f'<span class="zapio-badge">{badge}</span><br>' if badge else ""
    subtitle_html = f'<p style="color: #CBD5E1; font-size: 0.95rem; margin-top: 5px;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
        <div style="margin-top: 10px; margin-bottom: 20px;">
            {badge_html}
            <h2 style="margin-top: 8px; font-size: 2rem; color: #FFF;">{title}</h2>
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)
