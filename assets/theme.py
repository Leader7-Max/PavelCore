"""Thème centralisé de PavelCore : palettes de couleurs + blocs CSS partagés.

Le design global (champs, boutons, onglets, calendriers) reste dans assets/styles.py.
Ce fichier regroupe :
  - les palettes (THEMES) et get_theme() ;
  - le CSS de l'écran de connexion, des cartes de succès et du moteur d'alarmes.
"""

DEFAULT_THEME = "Sombre Nuit"

THEMES = {
    "Blanc Épuré": dict(
        text_color="#0F172A", sub_title_color="#0F172A", desc_color="#475569",
        header_box_bg="#F1F5F9", header_box_text="#475569",
        card_border="#E2E8F0", card_bg="#FFFFFF",
    ),
    "Sombre Nuit": dict(
        text_color="#F8FAFC", sub_title_color="#FFF", desc_color="#CBD5E1",
        header_box_bg="#1E0A3C", header_box_text="#A78BFA",
        card_border="#2B1552", card_bg="#170A2E",
    ),
}


def get_theme(name=None) -> dict:
    """Retourne la palette demandée (palette sombre par défaut si le nom est inconnu)."""
    return dict(THEMES.get(name or DEFAULT_THEME, THEMES[DEFAULT_THEME]))


# ── CSS des boutons Connexion / Inscription & cartes de succès ─
AUTH_SWITCH_CSS = """
<style>
.st-key-auth_switch [data-testid="stHorizontalBlock"]{
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
}
.st-key-auth_switch [data-testid="stColumn"],
.st-key-auth_switch [data-testid="column"]{
    min-width: 0 !important;
    flex: 1 1 0 !important;
    width: auto !important;
}
.st-key-auth_switch button{
    width: 100% !important;
    border-radius: 50px !important;
    padding: 12px 8px !important;
    box-shadow: 0 4px 12px rgba(236,72,153,0.3) !important;
    transition: none !important;
}
.st-key-auth_switch button p{
    color: #FFF !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
}
/* Bouton actif */
.st-key-auth_switch button[kind="primary"],
.st-key-auth_switch button[data-testid="stBaseButton-primary"]{
    background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
}
/* Bouton inactif */
.st-key-auth_switch button[kind="secondary"],
.st-key-auth_switch button[data-testid="stBaseButton-secondary"]{
    background: #230E3D !important;
    border: 1px solid rgba(236,72,153,0.4) !important;
}

/* Design Card Message Succès Inscription */
.pavel-auth-success-card {
    background: linear-gradient(135deg, rgba(35, 14, 61, 0.95) 0%, rgba(23, 10, 46, 0.95) 100%) !important;
    border: 1px solid rgba(236, 72, 153, 0.5) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    margin-top: 15px !important;
    box-shadow: 0 8px 25px rgba(236, 72, 153, 0.25) !important;
    display: flex !important;
    align-items: center !important;
    gap: 15px !important;
}

/* Design Card Connexion Réussie */
.pavel-login-success-banner {
    background: linear-gradient(135deg, rgba(30, 10, 60, 0.95) 0%, rgba(15, 5, 30, 0.98) 100%) !important;
    border: 2px solid #EC4899 !important;
    border-radius: 16px !important;
    padding: 18px 22px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4), inset 0 0 15px rgba(139, 92, 246, 0.2) !important;
    display: flex !important;
    align-items: center !important;
    gap: 18px !important;
    transition: opacity 0.8s ease-out;
}

/* Design Card Coffre-Fort Sécurisé */
.pavel-vault-success-banner {
    background: linear-gradient(135deg, rgba(30, 10, 60, 0.95) 0%, rgba(15, 5, 30, 0.98) 100%) !important;
    border: 2px solid #EC4899 !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4), inset 0 0 15px rgba(139, 92, 246, 0.2) !important;
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
}

/* Disparition automatique de la bannière de bienvenue (5 s visible, puis fondu 0,8 s) */
.pavel-welcome-wrap {
    overflow: hidden;
    animation: pavelWelcomeFade 5.8s ease-out forwards;
}
@keyframes pavelWelcomeFade {
    0%, 86% { opacity: 1; max-height: 240px; }
    100%    { opacity: 0; max-height: 0; }
}
</style>
"""

# ── Moteur d'alarmes invisible (toutes les rubriques sauf l'Agenda) ─
ENGINE_CSS = """
<style>
.st-key-pc_engine{
    position: absolute !important;
    width: 1px !important; height: 1px !important;
    overflow: hidden !important; opacity: 0 !important;
    pointer-events: none !important; margin: 0 !important; padding: 0 !important;
}
</style>
"""

# ── Styles des cartes, injectés aussi dans l'application connectée ─
# (conteneur invisible : aucun espace ajouté dans la mise en page)
APP_CSS = """
<style>
.st-key-pc_css{
    position: absolute !important;
    width: 1px !important; height: 1px !important;
    overflow: hidden !important; opacity: 0 !important;
    pointer-events: none !important; margin: 0 !important; padding: 0 !important;
}
</style>
""" + AUTH_SWITCH_CSS
