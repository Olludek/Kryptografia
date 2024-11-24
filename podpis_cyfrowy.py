import os
import hashlib
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

# Ścieżki do przechowywania kluczy
KEY_FOLDER = 'keys'
PRIVATE_KEY_PATH = os.path.join(KEY_FOLDER, 'private_key.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_FOLDER, 'public_key.pem')

def generate_rsa_keys():
    """
    Generuje parę kluczy RSA (prywatny i publiczny) i zapisuje je w plikach.

    :return: Tuple zawierające klucz prywatny i publiczny jako obiekty.
    """
    # Tworzenie katalogu na klucze, jeśli nie istnieje
    os.makedirs(KEY_FOLDER, exist_ok=True)
    
    # Generowanie klucza prywatnego RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Wykładnik publiczny
        key_size=2048,          # Długość klucza w bitach
    )
    
    # Zapis klucza prywatnego do pliku w formacie PEM
    with open(PRIVATE_KEY_PATH, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,                    # Kodowanie PEM
            format=serialization.PrivateFormat.PKCS8,               # Format PKCS8
            encryption_algorithm=serialization.NoEncryption()        # Brak szyfrowania klucza
        ))
    
    # Pobieranie klucza publicznego z klucza prywatnego
    public_key = private_key.public_key()
    
    # Zapis klucza publicznego do pliku w formacie PEM
    with open(PUBLIC_KEY_PATH, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,                    # Kodowanie PEM
            format=serialization.PublicFormat.SubjectPublicKeyInfo    # Format PublicKeyInfo
        ))
    
    return private_key, public_key

def load_private_key():
    """
    Ładuje klucz prywatny z pliku.

    :return: Obiekt klucza prywatnego RSA.
    """
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,  # Brak hasła do klucza prywatnego
        )
    return private_key

def load_public_key():
    """
    Ładuje klucz publiczny z pliku.

    :return: Obiekt klucza publicznego RSA.
    """
    with open(PUBLIC_KEY_PATH, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
        )
    return public_key

def sign_data(data):
    """
    Generuje podpis cyfrowy dla podanych danych.

    :param data: Dane do podpisania (bytes).
    :return: Podpis cyfrowy jako string w formacie Base64.
    """
    private_key = load_private_key()
    
    # Tworzenie podpisu cyfrowego za pomocą klucza prywatnego
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),  # Mask Generation Function
            salt_length=padding.PSS.MAX_LENGTH  # Długość soli
        ),
        hashes.SHA256()  # Funkcja skrótu
    )
    
    # Kodowanie podpisu do formatu Base64
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(data, signature):
    """
    Weryfikuje podpis cyfrowy dla podanych danych.

    :param data: Dane, które zostały podpisane (bytes).
    :param signature: Podpis cyfrowy w formacie Base64 (string).
    :return: True jeśli podpis jest prawidłowy, False w przeciwnym razie.
    """
    public_key = load_public_key()
    signature = base64.b64decode(signature)  # Dekodowanie podpisu z Base64
    
    try:
        # Weryfikacja podpisu za pomocą klucza publicznego
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),  # Musi odpowiadać paddingowi użytemu podczas podpisywania
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True  # Podpis jest prawidłowy
    except Exception as e:
        print(f"Weryfikacja podpisu nie powiodła się: {e}")
        return False  # Podpis jest nieprawidłowy lub dane zostały zmienione

def hash_file(file_path):
    """
    Obliczenie hash SHA-256 dla podanego pliku.

    :param file_path: Ścieżka do pliku.
    :return: Skrót SHA-256 jako bytes.
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Czytanie pliku w kawałkach po 4096 bajtów
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.digest()
