from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Maksymalny rozmiar bloku dla klucza 2048-bitowego (pomniejszony dla paddingu)
RSA_MAX_BLOCK_SIZE = 200

# Funkcja generująca parę kluczy RSA
def generuj_klucze():
    """
    Generuje parę kluczy RSA (prywatny i publiczny).

    :return: Tuple zawierające klucz prywatny i publiczny jako stringi.
    """
    key = RSA.generate(2048)  # Generowanie klucza RSA o długości 2048 bitów
    private_key = key.export_key().decode('utf-8').strip()  # Eksport klucza prywatnego w formacie PEM
    public_key = key.publickey().export_key().decode('utf-8').strip()  # Eksport klucza publicznego w formacie PEM
    return private_key, public_key

# Funkcja dzieląca dane na bloki o określonym rozmiarze
def split_into_blocks(data, block_size):
    """
    Dzieli dane na bloki o określonym rozmiarze.

    :param data: Dane do podziału (bytes).
    :param block_size: Rozmiar pojedynczego bloku (int).
    :return: Lista bloków danych.
    """
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]

# Funkcja szyfrująca przy użyciu klucza publicznego RSA (dla większych plików)
def szyfruj_rsa(data, public_key):
    """
    Szyfruje dane za pomocą klucza publicznego RSA.

    :param data: Tekst do zaszyfrowania (string).
    :param public_key: Klucz publiczny RSA (string w formacie PEM).
    :return: Zaszyfrowane dane jako string w formacie Base64.
    """
    key = RSA.import_key(public_key.strip())  # Import klucza publicznego
    cipher = PKCS1_OAEP.new(key)  # Inicjalizacja szyfratora z paddingiem PKCS1_OAEP

    # Dzielimy dane na bloki o rozmiarze RSA_MAX_BLOCK_SIZE
    blocks = split_into_blocks(data.encode('utf-8'), RSA_MAX_BLOCK_SIZE)
    # Szyfrujemy każdy blok i kodujemy go w Base64
    encrypted_blocks = [base64.b64encode(cipher.encrypt(block)).decode('utf-8') for block in blocks]
    
    # Łączymy zaszyfrowane bloki, dodając separator (newline)
    return '\n'.join(encrypted_blocks)

# Funkcja deszyfrująca przy użyciu klucza prywatnego RSA (dla większych plików)
def deszyfruj_rsa(data, private_key):
    """
    Deszyfruje dane za pomocą klucza prywatnego RSA.

    :param data: Zaszyfrowane dane w formacie Base64 (string).
    :param private_key: Klucz prywatny RSA (string w formacie PEM).
    :return: Odszyfrowane dane jako string.
    """
    key = RSA.import_key(private_key.strip())  # Import klucza prywatnego
    cipher = PKCS1_OAEP.new(key)  # Inicjalizacja deszyfratora z paddingiem PKCS1_OAEP

    # Dzielimy zaszyfrowany tekst na bloki (rozdzielone newline)
    encrypted_blocks = data.split('\n')
    decrypted_blocks = []
    for block in encrypted_blocks:
        try:
            # Deszyfrowanie każdego bloku po jego dekodowaniu z Base64
            decrypted_block = cipher.decrypt(base64.b64decode(block))
            decrypted_blocks.append(decrypted_block.decode('utf-8'))
        except (ValueError, TypeError, base64.binascii.Error) as e:
            print(f"Błąd podczas deszyfrowania bloku: {e}")
            return "Deszyfrowanie nie powiodło się: Sprawdź zaszyfrowane dane i klucz prywatny."

    # Łączymy odszyfrowane bloki w pełny tekst
    return ''.join(decrypted_blocks)
