import streamlit as st
from database import supabase, supabase_admin
from auth import require_admin


def show():
    require_admin()
    st.title("Administración de usuarios y roles")

    tab1, tab2 = st.tabs(["Usuarios y roles", "Crear usuario"])

    with tab1:
        _tab_usuarios()

    with tab2:
        _tab_crear_usuario()


def _tab_usuarios():
    st.subheader("Usuarios registrados")

    # Obtener todos los perfiles con sus roles
    profiles_res = supabase.table("profiles").select("id, full_name, created_at").execute()
    profiles = profiles_res.data or []

    roles_cat_res = supabase.table("roles").select("id, name, description").execute()
    roles_catalogo = roles_cat_res.data or []
    roles_map = {r["id"]: r["name"] for r in roles_catalogo}
    roles_opciones = {r["name"]: r["id"] for r in roles_catalogo}

    if not profiles:
        st.info("No hay usuarios registrados.")
        return

    for profile in profiles:
        uid = profile["id"]
        name = profile["full_name"] or "(sin nombre)"

        # Roles actuales del usuario
        ur_res = supabase.table("user_roles").select("role_id").eq("user_id", uid).execute()
        roles_actuales_ids = [r["role_id"] for r in (ur_res.data or [])]
        roles_actuales_nombres = [roles_map.get(rid, "") for rid in roles_actuales_ids]

        with st.expander(f"{name}  —  {', '.join(roles_actuales_nombres) or 'sin rol'}"):
            st.caption(f"ID: `{uid}`")
            st.caption(f"Creado: {profile['created_at'][:10]}")

            col1, col2 = st.columns([3, 1])
            with col1:
                seleccion = st.multiselect(
                    "Roles asignados",
                    options=list(roles_opciones.keys()),
                    default=roles_actuales_nombres,
                    key=f"roles_{uid}"
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("Guardar", key=f"save_{uid}"):
                    _actualizar_roles(uid, seleccion, roles_opciones)
                    st.success("Roles actualizados.")
                    st.rerun()


def _actualizar_roles(user_id: str, nuevos_roles: list[str], roles_opciones: dict):
    # Eliminar todos los roles actuales
    supabase.table("user_roles").delete().eq("user_id", user_id).execute()

    # Insertar los nuevos
    if nuevos_roles:
        nuevos = [{"user_id": user_id, "role_id": roles_opciones[r]} for r in nuevos_roles]
        supabase.table("user_roles").insert(nuevos).execute()


def _tab_crear_usuario():
    st.subheader("Crear nuevo usuario")

    roles_res = supabase.table("roles").select("id, name").execute()
    roles_catalogo = roles_res.data or []
    roles_opciones = {r["name"]: r["id"] for r in roles_catalogo}

    with st.form("form_crear_usuario"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Nombre completo")
            email = st.text_input("Email")
        with col2:
            password = st.text_input("Contraseña", type="password")
            roles_sel = st.multiselect("Roles", options=list(roles_opciones.keys()))

        submitted = st.form_submit_button("Crear usuario", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Email y contraseña son obligatorios.")
            else:
                _crear_usuario(email, password, full_name, roles_sel, roles_opciones)


def _crear_usuario(email: str, password: str, full_name: str, roles: list[str], roles_opciones: dict):
    try:
        res = supabase_admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"full_name": full_name}
        })
        user_id = res.user.id

        # El trigger en Supabase crea el profile automáticamente,
        # pero actualizamos full_name por si acaso
        supabase.table("profiles").upsert({
            "id": user_id,
            "full_name": full_name
        }).execute()

        # Asignar roles
        if roles:
            nuevos = [{"user_id": user_id, "role_id": roles_opciones[r]} for r in roles]
            supabase.table("user_roles").insert(nuevos).execute()

        st.success(f"Usuario {email} creado correctamente.")
        st.rerun()

    except Exception as e:
        st.error(f"Error al crear usuario: {e}")
