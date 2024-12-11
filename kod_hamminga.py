# kod_hamminga.py

def generuj_kod_hamminga(dane):
    """
    Funkcja generuje kod Hamminga dla danego ciągu danych binarnych.
    
    :param dane: Ciąg bitów do zakodowania (jako lista [0,1,1,0,...]).
    :return: Zakodowany ciąg danych z kodem Hamminga.
    """
    n = len(dane)
    r = 0
    # Liczymy najmniejszą liczbę bitów parzystości r
    while (2**r - r - 1) < n:
        r += 1

    # Inicjalizacja wynikowego kodu Hamminga
    kod_hamminga = [0] * (n + r)
    
    j = 0
    # Wstawiamy dane do wynikowego kodu, pomijając miejsca dla bitów parzystości
    for i in range(n + r):
        if (i + 1) & (i) == 0:
            kod_hamminga[i] = 0  # Miejsce na bit parzystości
        else:
            kod_hamminga[i] = dane[j]
            j += 1

    # Obliczanie bitów parzystości
    for i in range(r):
        bit = 0
        for j in range(1, n + r + 1):
            if j & (2**i) > 0:
                bit ^= kod_hamminga[j - 1]
        kod_hamminga[2**i - 1] = bit
    
    return kod_hamminga
