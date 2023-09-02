def validate_auth_form(form: dict) -> str:
    username = form.get("username")
    password = form.get("password")

    if not username:
        return "Username is required."

    if not password:
        return "Password is required."

    return ""
