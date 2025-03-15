# utils.py
import hashlib

def generate_activation_key(serial_number):
    # Utilisez un sel (salt) pour renforcer la sécurité
    salt = "votre_secret_salt"
    data = f"{serial_number}-{salt}"
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()[:16]  # Retourne une clé de 16 caractères