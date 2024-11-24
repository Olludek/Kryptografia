import string

# Funkcja do szyfrowania tekstu za pomocą szyfru Rail Fence
def szyfruj_rail_fence(text, key):
    """
    Szyfruje podany tekst używając szyfru Rail Fence z określoną liczbą szyn.
    
    :param text: Tekst do zaszyfrowania.
    :param key: Liczba szyn.
    :return: Zaszyfrowany tekst oraz wizualizacja zygzaka.
    """
    # Tworzenie tablicy wypełnionej pustymi stringami do zapisu zygzaka
    rail = [['' for _ in range(len(text))] for _ in range(key)]
    direction_down = False  # Kierunek pisania zygzaka
    row, col = 0, 0  # Początkowa pozycja w tablicy

    # Przechodzimy przez tekst i zapisujemy go zygzakowato
    for char in text:
        rail[row][col] = char  # Umieszczanie znaku w odpowiedniej pozycji
        col += 1  # Przejście do następnej kolumny
        # Zmiana kierunku, gdy osiągniemy górną lub dolną szynę
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        # Przejście w dół lub w górę w zależności od kierunku
        row += 1 if direction_down else -1

    # Zbieramy wynik szyfrowania, odczytując tekst poziomami szyn
    result = ''.join([''.join(rail[i]) for i in range(key)])
    return result, rail  # Zwracamy zaszyfrowany tekst i strukturę tablicy

# Funkcja do deszyfrowania tekstu za pomocą szyfru Rail Fence
def deszyfruj_rail_fence(text, key):
    """
    Deszyfruje podany tekst używając szyfru Rail Fence z określoną liczbą szyn.
    
    :param text: Tekst do odszyfrowania.
    :param key: Liczba szyn.
    :return: Odszyfrowany tekst oraz zygzakowata struktura.
    """
    # Tworzenie tablicy wypełnionej pustymi stringami do odczytu zygzaka
    rail = [['' for _ in range(len(text))] for _ in range(key)]
    direction_down = None  # Kierunek pisania zygzaka
    row, col = 0, 0  # Początkowa pozycja w tablicy

    # Tworzenie wzoru zygzaka, oznaczając miejsca, gdzie będą znaki
    for i in range(len(text)):
        rail[row][col] = '*'  # Oznaczenie miejsca na znak
        col += 1  # Przejście do następnej kolumny
        if row == 0:
            direction_down = True  # Zmiana kierunku na w dół
        elif row == key - 1:
            direction_down = False  # Zmiana kierunku na w górę
        # Przejście w dół lub w górę w zależności od kierunku
        row += 1 if direction_down else -1

    # Wstawianie zaszyfrowanego tekstu do zygzaka
    index = 0  # Indeks do iteracji po tekście
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] == '*' and index < len(text):
                rail[i][j] = text[index]  # Wstawianie znaku w odpowiednie miejsce
                index += 1

    # Odczytujemy tekst w zygzaku
    result = []
    row, col = 0, 0  # Resetowanie pozycji
    for i in range(len(text)):
        result.append(rail[row][col])  # Dodanie znaku do wyniku
        col += 1  # Przejście do następnej kolumny
        if row == 0:
            direction_down = True  # Zmiana kierunku na w dół
        elif row == key - 1:
            direction_down = False  # Zmiana kierunku na w górę
        # Przejście w dół lub w górę w zależności od kierunku
        row += 1 if direction_down else -1
    return ''.join(result), rail  # Zwracamy odszyfrowany tekst i strukturę tablicy

# Funkcja do szyfrowania lub deszyfrowania pliku za pomocą szyfru Rail Fence
def przetworz_pliki_rail_fence(file_path, key, operation_func):
    """
    Przetwarza plik tekstowy, szyfrując lub deszyfrując jego zawartość za pomocą szyfru Rail Fence.
    
    :param file_path: Ścieżka do pliku tekstowego.
    :param key: Liczba szyn.
    :param operation_func: Funkcja operacji (szyfruj_rail_fence lub deszyfruj_rail_fence).
    :return: Ścieżka do przetworzonego pliku.
    """
    # Odczytanie zawartości pliku
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Przetworzenie zawartości za pomocą wybranej funkcji
    result, _ = operation_func(content, key)
    # Tworzenie ścieżki do nowego pliku z dodanym sufiksem
    processed_file_path = f"{file_path}_processed.txt"
    # Zapisanie przetworzonej zawartości do nowego pliku
    with open(processed_file_path, 'w', encoding='utf-8') as file:
        file.write(result)
    return processed_file_path  # Zwrócenie ścieżki do przetworzonego pliku
