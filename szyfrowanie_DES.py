from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

# Funkcja do szyfrowania przy użyciu DES
def szyfruj_des(data, key, mode='ECB', iv=None):
    """
    Szyfruje podane dane za pomocą algorytmu DES.
    
    :param data: Tekst do zaszyfrowania (string).
    :param key: Klucz szyfrujący (8 znaków).
    :param mode: Tryb pracy DES (ECB, CBC, OFB).
    :param iv: Wektor inicjalizacji (IV) - wymagany dla trybów CBC i OFB.
    :return: Zaszyfrowane dane w formacie Base64 (string).
    """
    # Konwersja klucza i danych na bajty
    key = key.encode('utf-8')
    data = data.encode('utf-8')
    # Ustalenie IV, jeśli jest wymagany; domyślnie 8 zerowych bajtów
    iv = iv.encode('utf-8') if iv else b'\0' * 8

    # Wybór trybu szyfrowania na podstawie parametru
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)

    # Szyfrowanie danych z odpowiednim paddingiem
    if mode in ['ECB', 'CBC']:
        encrypted_data = cipher.encrypt(pad(data, DES.block_size))
    else:
        encrypted_data = cipher.encrypt(data)
    
    # Kodowanie zaszyfrowanych danych do formatu Base64
    return base64.b64encode(encrypted_data).decode('utf-8')

# Funkcja do deszyfrowania przy użyciu DES
def deszyfruj_des(data, key, mode='ECB', iv=None):
    """
    Deszyfruje podane dane za pomocą algorytmu DES.
    
    :param data: Zaszyfrowane dane w formacie Base64 (string).
    :param key: Klucz deszyfrujący (8 znaków).
    :param mode: Tryb pracy DES (ECB, CBC, OFB).
    :param iv: Wektor inicjalizacji (IV) - wymagany dla trybów CBC i OFB.
    :return: Odszyfrowane dane jako string.
    """
    # Konwersja klucza na bajty
    key = key.encode('utf-8')
    # Dekodowanie danych z formatu Base64
    data = base64.b64decode(data)
    # Ustalenie IV, jeśli jest wymagany; domyślnie 8 zerowych bajtów
    iv = iv.encode('utf-8') if iv else b'\0' * 8

    # Wybór trybu deszyfrowania na podstawie parametru
    if mode == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif mode == 'OFB':
        cipher = DES.new(key, DES.MODE_OFB, iv)

    # Deszyfrowanie danych
    decrypted_data = cipher.decrypt(data)
    # Usunięcie paddingu, jeśli jest wymagane
    if mode in ['ECB', 'CBC']:
        try:
            decrypted_data = unpad(decrypted_data, DES.block_size)
        except ValueError:
            raise ValueError("Nieprawidłowy klucz lub uszkodzone dane.")
    
    # Konwersja bajtów na string
    return decrypted_data.decode('utf-8')

