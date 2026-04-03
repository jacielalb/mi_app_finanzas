import streamlit as st
from database import supabase


def login(email: str, password: str) -> tuple[bool, str]:
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        session = res.session

        # Guardar tokens para restaurar sesión en reruns
        st.session_state.access_token = session.access_token
        st.session_state.refresh_token = session.refresh_token

        # Obtener roles del usuario
        roles_res = supabase.table("user_roles").select(
            "roles(name)"
        ).eq("user_id", user.id).execute()

        roles = [r["roles"]["name"] for r in roles_res.data if r.get("roles")]

        # Obtener nombre del perfil
        profile_res = supabase.table("profiles").select("full_name").eq("id", user.id).execute()
        full_name = (profile_res.data[0]["full_name"] or user.email) if profile_res.data else user.email

        st.session_state.logged_in = True
        st.session_state.user_id = user.id
        st.session_state.user_email = user.email
        st.session_state.user_name = full_name
        st.session_state.roles = roles

        return True, ""
    except Exception as e:
        return False, str(e)


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for key in ["logged_in", "user_id", "user_email", "user_name", "roles",
                "access_token", "refresh_token"]:
        st.session_state.pop(key, None)


def restore_session():
    """Restaura la sesión del usuario en el cliente de Supabase (necesario tras reruns)."""
    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")
    if access_token and refresh_token:
        try:
            supabase.auth.set_session(access_token, refresh_token)
        except Exception:
            pass


def has_role(role: str) -> bool:
    return role in st.session_state.get("roles", [])


def is_admin() -> bool:
    return has_role("admin")


def is_editor() -> bool:
    return has_role("editor") or has_role("admin")


def require_login():
    if not st.session_state.get("logged_in"):
        st.error("Debes iniciar sesión para acceder.")
        st.stop()


def require_role(role: str):
    require_login()
    if not has_role(role):
        st.error(f"No tienes permiso para acceder a esta sección. Se requiere rol: {role}.")
        st.stop()


def require_admin():
    require_login()
    if not is_admin():
        st.error("Esta sección es solo para administradores.")
        st.stop()
