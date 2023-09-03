def validate_post_form(form: dict) -> str:
    title = form.get("title")
    body = form.get("body")

    if not title:
        return "Title is required."

    if not body:
        return "Body is required."

    return ""
