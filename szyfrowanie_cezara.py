import string

# Funkcja do szyfrowania tekstu za pomocą szyfru Cezara
def szyfruj_cezara(text, shift):
    """
    Szyfruje podany tekst przesuwając każdą literę o określoną liczbę miejsc.
    
    :param text: Tekst do zaszyfrowania.
    :param shift: Liczba miejsc do przesunięcia liter.
    :return: Zaszyfrowany tekst.
    """
    result = []
    for char in text:
        if char.isalpha():  # Sprawdzenie, czy znak jest literą
            # Ustalenie podstawy przesunięcia (A lub a)
            shift_base = ord('A') if char.isupper() else ord('a')
            # Obliczenie nowej litery po przesunięciu
            result.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            # Dodanie niealfabetycznych znaków bez zmian
            result.append(char)
    return ''.join(result)

# Funkcja do deszyfrowania tekstu za pomocą szyfru Cezara
def deszyfruj_cezara(text, shift):
    """
    Deszyfruje podany tekst przesuwając każdą literę o określoną liczbę miejsc w przeciwnym kierunku.
    
    :param text: Tekst do odszyfrowania.
    :param shift: Liczba miejsc do przesunięcia liter.
    :return: Odszyfrowany tekst.
    """
    return szyfruj_cezara(text, -shift)  # Przesunięcie w przeciwnym kierunku

# Funkcja do szyfrowania lub deszyfrowania pliku za pomocą szyfru Cezara
def przetworz_pliki_cezara(file_path, shift, operation_func):
    """
    Przetwarza plik tekstowy, szyfrując lub deszyfrując jego zawartość.
    
    :param file_path: Ścieżka do pliku tekstowego.
    :param shift: Liczba miejsc do przesunięcia liter.
    :param operation_func: Funkcja operacji (szyfruj_cezara lub deszyfruj_cezara).
    :return: Ścieżka do przetworzonego pliku.
    """
    # Odczytanie zawartości pliku
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Przetworzenie zawartości za pomocą wybranej funkcji
    result = operation_func(content, shift)
    
    # Tworzenie ścieżki do nowego pliku z dodanym sufiksem
    encrypted_file_path = f"{file_path}_encrypted.txt"
    # Zapisanie przetworzonej zawartości do nowego pliku
    with open(encrypted_file_path, 'w', encoding='utf-8') as file:
        file.write(result)
    
    return encrypted_file_path  # Zwrócenie ścieżki do przetworzonego pliku
