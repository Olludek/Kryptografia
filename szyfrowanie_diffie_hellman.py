import random

# Funkcja do generowania klucza publicznego na podstawie klucza prywatnego i ustalonej wartości g oraz p
def generuj_klucz_publiczny(prywatny_klucz, g, p):
    """
    Generuje klucz publiczny na podstawie klucza prywatnego i parametrów g oraz p.
    
    :param prywatny_klucz: Prywatny klucz użytkownika (int).
    :param g: Podstawa (g) w protokole Diffie-Hellmana (int).
    :param p: Moduł (p) w protokole Diffie-Hellmana (int).
    :return: Klucz publiczny (int).
    """
    return pow(g, prywatny_klucz, p)

# Funkcja do generowania wspólnego klucza na podstawie klucza publicznego drugiej strony oraz klucza prywatnego
def generuj_wspolny_klucz(publiczny_klucz_innej_osoby, prywatny_klucz, p):
    """
    Generuje wspólny klucz szyfrujący na podstawie klucza publicznego drugiej osoby oraz własnego klucza prywatnego.
    
    :param publiczny_klucz_innej_osoby: Klucz publiczny drugiej osoby (int).
    :param prywatny_klucz: Własny klucz prywatny (int).
    :param p: Moduł (p) w protokole Diffie-Hellmana (int).
    :return: Wspólny klucz szyfrujący (int).
    """
    return pow(publiczny_klucz_innej_osoby, prywatny_klucz, p)

# Funkcja do generowania losowego klucza prywatnego
def generuj_klucz_prywatny():
    """
    Generuje losowy klucz prywatny dla użytkownika.
    
    :return: Losowy klucz prywatny (int).
    """
    return random.randint(1000, 9999)  # Generuje losowy klucz w zakresie od 1000 do 9999
