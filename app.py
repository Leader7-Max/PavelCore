col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if "auth_mode" not in st.session_state:
            st.session_state.auth_mode = "login"

        # CSS anti-empilement mobile pour forcer ces 2 colonnes à rester côte à côte
        st.markdown("""
            <style>
                @media (max-width: 640px) {
                    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                        width: 50% !important;
                        flex: 1 1 50% !important;
                        min-width: unset !important;
                    }
                }
            </style>
        """, unsafe_allow_html=True)

        # 1. Boutons d'authentification instantanés côte à côte
        auth_col1, auth_col2 = st.columns(2)
        with auth_col1:
            if st.button("🔑 Connexion", use_container_width=True, type="primary" if st.session_state.auth_mode == "login" else "secondary"):
                st.session_state.auth_mode = "login"
                st.rerun()
        with auth_col2:
            if st.button("✨ Inscription", use_container_width=True, type="primary" if st.session_state.auth_mode == "signup" else "secondary"):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Bouton d'accès direct à l'Agenda repositionné ICI (juste après les onglets, avant le formulaire)
        if st.button("📅 Accéder directement à l'Agenda (Mode Démo / Hors-ligne)", use_container_width=True, type="secondary"):
            st.session_state.direct_agenda =True
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Formulaires dynamiques (Connexion ou Inscription)
        if st.session_state.auth_mode == "login":
            with st.form("login_form"):
                email = st.text_input("Adresse Email", placeholder="votre.email@exemple.com", key="login_email")
                password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")
                submit_login = st.form_submit_button("Se connecter au Workspace", use_container_width=True)
                
                if submit_login:
                    ok, res = authenticate_user_db(email, password)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_info = res
                        st.toast(f"🔓 Bienvenue, {res['email']} !", icon="✨")
                        st.rerun()
                    else:
                        st.error(res)
        else:
            with st.form("signup_form"):
                new_email = st.text_input("Adresse Email", placeholder="nom@exemple.com", key="signup_email")
                new_pass = st.text_input("Créer un mot de passe", type="password", placeholder="••••••••", key="signup_pass")
                confirm_pass = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••", key="signup_confirm_pass")
                submit_signup = st.form_submit_button("S'inscrire et rejoindre PavelCore", use_container_width=True)
                
                if submit_signup:
                    if new_pass != confirm_pass:
                        st.error("Les deux mots de passe ne correspondent pas.")
                    elif len(new_pass) < 6:
                        st.warning("Le mot de passe doit contenir au moins 6 caractères.")
                    else:
                        ok, msg = create_user_db(new_email, new_pass)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
