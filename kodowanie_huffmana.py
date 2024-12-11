import heapq
from collections import defaultdict

class Węzeł:
    def __init__(self, litera, częstotliwość):
        self.litera = litera
        self.częstotliwość = częstotliwość
        self.lewy = None
        self.prawy = None

    def __lt__(self, other):
        return self.częstotliwość < other.częstotliwość

def buduj_kodowanie_huffmana(tekst):
    # Liczymy częstotliwość występowania każdej litery
    częstotliwość = defaultdict(int)
    for litera in tekst:
        częstotliwość[litera] += 1

    # Tworzymy kolejkę priorytetową
    kolejka = [Węzeł(litera, częstotliwość[litera]) for litera in częstotliwość]
    heapq.heapify(kolejka)

    # Budowanie drzewa Huffmana
    while len(kolejka) > 1:
        lewy = heapq.heappop(kolejka)
        prawy = heapq.heappop(kolejka)
        wezel = Węzeł(None, lewy.częstotliwość + prawy.częstotliwość)
        wezel.lewy = lewy
        wezel.prawy = prawy
        heapq.heappush(kolejka, wezel)

    # Drzewo Huffmana zostało zbudowane. Teraz tworzymy kodowanie
    korzeń = kolejka[0]
    kodowanie = {}

    def koduj_wezel(wezel, kod=""):
        if wezel is not None:
            if wezel.litera is not None:
                kodowanie[wezel.litera] = kod
            koduj_wezel(wezel.lewy, kod + "0")
            koduj_wezel(wezel.prawy, kod + "1")

    koduj_wezel(korzeń)

    return kodowanie, częstotliwość

def generuj_kod_huffmana(tekst):
    kodowanie, częstotliwość = buduj_kodowanie_huffmana(tekst)
    
    # Tworzymy wynikowy ciąg binarny
    kod_wynikowy = ''.join([kodowanie[litera] for litera in tekst])

    # Obliczamy częstotliwość liter w formie (litera, ilość, prawdopodobieństwo)
    czestotliwosc = [(litera, częstotliwość[litera], częstotliwość[litera] / len(tekst)) for litera in częstotliwość]
    
    return kod_wynikowy, czestotliwosc, kodowanie
