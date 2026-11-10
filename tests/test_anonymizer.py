import pytest
from src.anonymizer import hash_patient_id

def test_hash_patient_id_deterministic():
    id_1 = hash_patient_id("Bobby Jackson")
    id_2 = hash_patient_id("Bobby Jackson")
    assert id_1 == id_2
    assert id_1.startswith("PT-")

def test_hash_patient_id_case_insensitive():
    assert hash_patient_id("bobby jackson") == hash_patient_id("Bobby Jackson")

def test_hash_patient_id_rejects_empty():
    with pytest.raises(ValueError):
        hash_patient_id("")