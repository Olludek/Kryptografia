from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Funkcja do szyfrowania przy użyciu AES
def szyfruj_aes(data, key, mode='ECB', iv=None):
    """
    Szyfruje podane dane za pomocą algorytmu AES.
    
    :param data: Tekst do zaszyfrowania (string).
    :param key: Klucz szyfrujący (16, 24 lub 32 znaki).
    :param mode: Tryb pracy AES (ECB, CBC, OFB).
    :param iv: Wektor inicjalizacji (IV) - wymagany dla trybów CBC, OFB.
    :return: Zaszyfrowane dane w formacie Base64 (string).
    """
    # Konwersja klucza i danych na bajty
    key = key.encode('utf-8')
    data = data.encode('utf-8')
    # Ustalenie IV, jeśli jest wymagany; domyślnie 16 zerowych bajtów
    iv = iv.encode('utf-8') if iv else b'\0' * 16

    # Wybór trybu szyfrowania na podstawie parametru
    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == 'CBC':
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode == 'OFB':
        cipher = AES.new(key, AES.MODE_OFB, iv)

    # Szyfrowanie danych z odpowiednim paddingiem
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    # Kodowanie zaszyfrowanych danych do formatu Base64
    return base64.b64encode(encrypted_data).decode('utf-8')

# Funkcja do deszyfrowania przy użyciu AES
def deszyfruj_aes(data, key, mode='ECB', iv=None):
    """
    Deszyfruje podane dane za pomocą algorytmu AES.
    
    :param data: Zaszyfrowane dane w formacie Base64 (string).
    :param key: Klucz deszyfrujący (16, 24 lub 32 znaki).
    :param mode: Tryb pracy AES (ECB, CBC, OFB).
    :param iv: Wektor inicjalizacji (IV) - wymagany dla trybów CBC, OFB.
    :return: Odszyfrowane dane jako string.
    """
    # Konwersja klucza na bajty
    key = key.encode('utf-8')
    # Dekodowanie danych z formatu Base64
    data = base64.b64decode(data)
    # Ustalenie IV, jeśli jest wymagany; domyślnie 16 zerowych bajtów
    iv = iv.encode('utf-8') if iv else b'\0' * 16

    # Wybór trybu deszyfrowania na podstawie parametru
    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == 'CBC':
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode == 'OFB':
        cipher = AES.new(key, AES.MODE_OFB, iv)


    # Deszyfrowanie danych
    decrypted_data = cipher.decrypt(data)
    # Usunięcie paddingu, jeśli jest wymagane
    decrypted_data = unpad(decrypted_data, AES.block_size)
    
    # Konwersja bajtów na string
    return decrypted_data.decode('utf-8')
