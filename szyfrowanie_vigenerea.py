import string

# Funkcja do szyfrowania tekstu za pomocą szyfru Vigenère'a
def szyfruj_vigenerea(text, key):
    """
    Szyfruje podany tekst używając szyfru Vigenère'a z określonym kluczem.
    
    :param text: Tekst do zaszyfrowania.
    :param key: Klucz szyfrujący (słowo lub fraza).
    :return: Zaszyfrowany tekst.
    """
    key = key.upper()  # Konwersja klucza na wielkie litery
    result = []
    key_index = 0  # Indeks do iteracji po kluczu

    for char in text:
        if char.isalpha():  # Sprawdzenie, czy znak jest literą
            # Ustalenie podstawy przesunięcia (A lub a)
            shift_base = ord('A') if char.isupper() else ord('a')
            # Obliczenie wartości przesunięcia na podstawie klucza
            shift = ord(key[key_index % len(key)]) - ord('A')
            # Obliczenie nowej litery po przesunięciu
            result.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
            key_index += 1  # Przejście do kolejnej litery klucza
        else:
            # Dodanie niealfabetycznych znaków bez zmian
            result.append(char)
    return ''.join(result)

# Funkcja do deszyfrowania tekstu za pomocą szyfru Vigenère'a
def deszyfruj_vigenerea(text, key):
    """
    Deszyfruje podany tekst używając szyfru Vigenère'a z określonym kluczem.
    
    :param text: Tekst do odszyfrowania.
    :param key: Klucz deszyfrujący (słowo lub fraza).
    :return: Odszyfrowany tekst.
    """
    key = key.upper()  # Konwersja klucza na wielkie litery
    result = []
    key_index = 0  # Indeks do iteracji po kluczu

    for char in text:
        if char.isalpha():  # Sprawdzenie, czy znak jest literą
            # Ustalenie podstawy przesunięcia (A lub a)
            shift_base = ord('A') if char.isupper() else ord('a')
            # Obliczenie wartości przesunięcia na podstawie klucza
            shift = ord(key[key_index % len(key)]) - ord('A')
            # Obliczenie nowej litery po przesunięciu w przeciwnym kierunku
            result.append(chr((ord(char) - shift_base - shift) % 26 + shift_base))
            key_index += 1  # Przejście do kolejnej litery klucza
        else:
            # Dodanie niealfabetycznych znaków bez zmian
            result.append(char)
    return ''.join(result)

# Funkcja do szyfrowania lub deszyfrowania pliku za pomocą szyfru Vigenère'a
def przetworz_pliki_vigenerea(file_path, key, operation_func):
    """
    Przetwarza plik tekstowy, szyfrując lub deszyfrując jego zawartość za pomocą szyfru Vigenère'a.
    
    :param file_path: Ścieżka do pliku tekstowego.
    :param key: Klucz szyfrujący/deszyfrujący.
    :param operation_func: Funkcja operacji (szyfruj_vigenerea lub deszyfruj_vigenerea).
    :return: Ścieżka do przetworzonego pliku.
    """
    # Odczytanie zawartości pliku
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Przetworzenie zawartości za pomocą wybranej funkcji
    result = operation_func(content, key)
    
    # Tworzenie ścieżki do nowego pliku z dodanym sufiksem
    encrypted_file_path = f"{file_path}_encrypted.txt"
    # Zapisanie przetworzonej zawartości do nowego pliku
    with open(encrypted_file_path, 'w', encoding='utf-8') as file:
        file.write(result)
    
    return encrypted_file_path  # Zwrócenie ścieżki do przetworzonego pliku
