def read_secret(secret):
    # Read Docker secret from file system
    secret_path = f"/run/secrets/{secret}"

    try:
        with open(secret_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    