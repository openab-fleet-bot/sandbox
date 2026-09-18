def greet(name):
    if not isinstance(name, str):
        raise ValueError("name must be a string")

    stripped = name.strip()
    if not stripped:
        raise ValueError("name must not be empty or whitespace-only")

    return f"Hello, {stripped}!"
