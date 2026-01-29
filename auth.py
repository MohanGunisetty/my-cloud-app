import hashlib

def hash_password(password):
    """
    Hashes a password using SHA-256.
    
    Args:
        password (str): The plain text password.
        
    Returns:
        str: The hexdigest of the password.
    """
    if not password:
        raise ValueError("Password cannot be empty")
        
    # Convert string to bytes, verify consistent encoding (utf-8)
    password_bytes = password.encode('utf-8')
    
    # Create SHA256 hash
    hash_object = hashlib.sha256(password_bytes)
    
    # Return hex string (e.g., 'a94a8fe5...')
    return hash_object.hexdigest()

def verify_password_hash(plain_password, stored_hash):
    """
    Verifies if a password matches its hash.
    """
    return hash_password(plain_password) == stored_hash
