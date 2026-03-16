import bcrypt

SALT_PREFIX = "ujp"
SALT_SUFFIX = "ujp"

def _add_pepper(password: str) -> str:
    """Add prefix and suffix to password before hashing."""
    return SALT_PREFIX + password + SALT_SUFFIX

def hash_passwd(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    peppered = _add_pepper(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(peppered.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    peppered = _add_pepper(password)
    return bcrypt.checkpw(peppered.encode('utf-8'), hashed.encode('utf-8'))