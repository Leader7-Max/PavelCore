# AJOUTER CECI DANS assets/styles.py :
    st.markdown("""
        <style>
        /* Conteneur global de défilement horizontal type livre / carrousel */
        .horizontal-book-container {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 20px;
            padding-bottom: 20px;
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
        }

        .horizontal-book-container::-webkit-scrollbar {
            height: 6px;
        }
        .horizontal-book-container::-webkit-scrollbar-thumb {
            background: #EC4899;
            border-radius: 10px;
        }

        /* Chaque page/option s'aligne comme une page de livre */
        .book-page-panel {
            min-width: 100%;
            scroll-snap-align: start;
            flex-shrink: 0;
            transition: transform 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)
