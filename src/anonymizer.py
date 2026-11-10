import hashlib

def hash_patient_id(name: str, salt: str = "enterprise_phi_salt_2026") -> str:
    """
    Creates a deterministic, non-reversible surrogate ID from a patient name.
    Preserves referential integrity across admissions without exposing raw PHI.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Patient identifier must be a valid, non-empty string.")
    
    normalized = name.strip().lower()
    hashed = hashlib.sha256(f"{normalized}_{salt}".encode("utf-8")).hexdigest()
    return f"PT-{hashed[:10].upper()}"