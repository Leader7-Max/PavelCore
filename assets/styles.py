/* =========================================================
               CORRECTION RADICALE DU CONTENEUR BLANC DE L'UPLOADER
               ========================================================= */
            
            /* Cible la boîte principale de l'uploadeur et force un fond sombre aux accents néons */
            div[data-testid="stFileUploader"],
            section[data-testid="stFileUploaderDropzone"],
            div[data-baseweb="file-uploader"] {
                background-color: #230E3D !important;
                border: 2px dashed #EC4899 !important;
                border-radius: 12px !important;
                padding: 20px !important;
            }

            /* Force tous les textes, étiquettes et instructions internes en blanc ou gris clair */
            div[data-testid="stFileUploader"] * {
                color: #FFFFFF !important;
            }

            div[data-testid="stFileUploader"] small {
                color: #CBD5E1 !important;
            }

            /* Stylise le bouton interne de sélection de fichier */
            div[data-testid="stFileUploader"] button {
                background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border-radius: 8px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4) !important;
            }
