import os
from pyfidelius.cryptography import Cryptography

cryptography = Cryptography()


def test_generate_key_material():
    key_material = cryptography.generate_key_material()
    assert isinstance(key_material, dict)
    assert "privateKey" in key_material
    assert "x509PublicKey" in key_material
    assert "nonce" in key_material


def test_encrypt():
    data_to_encrypt = cryptography.encrypt(
        string_to_encrypt="Hello World!!",
        sender_nonce="lmXgblZwotx+DfBgKJF0lZXtAXgBEYr5khh79Zytr2Y=",
        requester_nonce="6uj1RdDUbcpI3lVMZvijkMC8Te20O4Bcyz0SyivX8Eg=",
        sender_private_key="AYhVZpbVeX4KS5Qm/W0+9Ye2q3rnVVGmqRICmseWni4=",
        requester_private_key="BAheD5rUqTy4V5xR4/6HWmYpopu5CO+KO8BECS0udNqUTSNo91TIqIIy1A4Vh+F94c+n9vAcwXU2bGcfsI5f69Y=",
    )
    assert isinstance(data_to_encrypt, dict)
    assert "encryptedData" in data_to_encrypt


def test_sane_encrypt():
    encrypted_data = cryptography.encrypt(
        string_to_encrypt="SGVsbG8gV29ybGRweXRlc3QgLg==",
        sender_nonce="lmXgblZwotx+DfBgKJF0lZXtAXgBEYr5khh79Zytr2Y=",
        requester_nonce="6uj1RdDUbcpI3lVMZvijkMC8Te20O4Bcyz0SyivX8Eg=",
        sender_private_key="AYhVZpbVeX4KS5Qm/W0+9Ye2q3rnVVGmqRICmseWni4=",
        requester_private_key="BAheD5rUqTy4V5xR4/6HWmYpopu5CO+KO8BECS0udNqUTSNo91TIqIIy1A4Vh+F94c+n9vAcwXU2bGcfsI5f69Y=",
    )
    assert isinstance(encrypted_data, dict)
    assert "encryptedData" in encrypted_data


def test_decrypt():
    decryptes_data = cryptography.decrypt(
        encrypted_data="uDkxVIgMaNEht/VqkQI1cYFgS7xm+Gc6y8Qh8dU=",
        sender_nonce="6uj1RdDUbcpI3lVMZvijkMC8Te20O4Bcyz0SyivX8Eg=",
        requester_nonce="lmXgblZwotx+DfBgKJF0lZXtAXgBEYr5khh79Zytr2Y=",
        sender_private_key="DMxHPri8d7IT23KgLk281zZenMfVHSdeamq0RhwlIBk=",
        requester_public_key="BABVt+mpRLMXiQpIfEq6bj8hlXsdtXIxLsspmMgLNI1SR5mHgDVbjHO2A+U4QlMddGzqyEidzm1AkhtSxSO2Ahg=",
    )
    assert isinstance(decryptes_data, dict)
    assert "decryptedData" in decryptes_data
    assert decryptes_data["decryptedData"] == "Hello World!!"


def test_file_operation_encryption():
    file_path = os.path.join(os.path.dirname(__file__), "encode_test.txt")
    file_encrypted = cryptography.file_operation(file_path)
    assert isinstance(file_encrypted, dict)
    assert "encryptedData" in file_encrypted


def test_file_operation_decryption():
    file_path = os.path.join(os.path.dirname(__file__), "decode_test.txt")
    file_decrypted = cryptography.file_operation(file_path)
    assert isinstance(file_decrypted, dict)
    assert "decryptedData" in file_decrypted
    assert file_decrypted["decryptedData"] == "Hello World!!"
