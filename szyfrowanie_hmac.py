import hmac
import hashlib

# Funkcja do generowania HMAC z użyciem SHA-256
def generuj_hmac_sha256(text, key):
    """
    Generuje kod HMAC z użyciem algorytmu SHA-256 dla podanego tekstu i klucza.
    
    :param text: Tekst, dla którego generujemy HMAC.
    :param key: Klucz tajny, który służy do generowania HMAC.
    :return: Wygenerowany HMAC w formie zakodowanej w base64.
    """
    hmac_obj = hmac.new(key.encode(), text.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

# Funkcja do weryfikacji HMAC
def weryfikuj_hmac_sha256(text, key, hmac_to_verify):
    """
    Weryfikuje, czy podany HMAC jest poprawny dla danego tekstu i klucza.
    
    :param text: Tekst, który chcemy zweryfikować.
    :param key: Klucz, który jest używany do weryfikacji HMAC.
    :param hmac_to_verify: HMAC, który chcemy sprawdzić.
    :return: True, jeśli HMAC jest poprawny, False w przeciwnym przypadku.
    """
    generated_hmac = generuj_hmac_sha256(text, key)
    return hmac.compare_digest(generated_hmac, hmac_to_verify)
