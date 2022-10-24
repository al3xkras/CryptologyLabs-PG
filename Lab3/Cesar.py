# Autorzy:
#  - Marek Jendernalik
#  - Maciej Nowosielski
#  - Michał Żylak

def wczytaj(a):
    nazwa_pliku = input("Podaj nazwę pliku tekstowego bez rozszerzenia: \nNazwa: ")
    try:
        t = open(nazwa_pliku + ".txt", "r")
        a = t.read()
        t.close()
        print(f"Wczytano plik " + nazwa_pliku + ".txt")

        return a, nazwa_pliku
    except:
        print("Niepoprawna nazwa pliku. \n")
        return wczytaj(a)


def przeksztalcenie(table, table2):
    size = range(len(table))
    for i in size:
        if i % 5 == 0 and i != 0 and i % 35 != 0:
            table2 = table2 + " "
        if i % 35 == 0 and i != 0:
            table2 = table2 + "\n"
        table2 = table2 + table[i]
    print(f"Przekształcono tekst")
    return table2


def inne_znaki(table):
    table = table.lower()

    # usuwamy symbole
    symbole = " .,'!:;/@#$%^&(*)-_+=[{]}|?\n\""
    d = range(len(symbole))
    for i in d:
        table = table.replace(symbole[i], "")

    # zamieniamy polskie znaki
    pl_znaki = "ąęółżźćńśĄĘÓŁŻŹĆŃŚ"
    pl_znaki2 = "aeolzzcnsAEOLZZCNS"
    c = range(len(pl_znaki))
    for i in c:
        table = table.replace(pl_znaki[i], pl_znaki2[i])

    print("Usunięto symbole i polskie znaki")
    return table


def Edit(table):
    table = inne_znaki(table)
    table = table.upper()
    return table


def Cesar(table):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = " 0123456789\n\""
    table = Edit(table)
    table2 = ""

    n = input("Podaj liczbę do kodu Cezara: ")
    try:
        n = int(n) % 26
    except:
        print("Nie podano liczby całkowitej!")
        return Cesar(table)

    a = input("Co chcesz zrobić z plikiem? (1-Zaszyfrować / 0-Odszyfrować): ")

    if a == "0":
        for char in table:
            if char in numbers:
                table2 = table2 + char
                continue
            i = (alphabet.index(char) - n) % 26
            table2 = table2 + alphabet[i]
        table2 = table2.lower()

    elif a == "1":
        for char in table:
            if char in numbers:
                table2 = table2 + char
                continue
            i = (alphabet.index(char) + n) % 26
            table2 = table2 + alphabet[i]

    else:
        print("Podano zły znak!")
        return Cesar(table)

    table3 = ""
    table3 = przeksztalcenie(table2, table3)

    return table3, a



def zapis(table2, nazwa_pliku, za_od):
    if za_od == "1":
        f = open(nazwa_pliku + "_za.txt", 'w')
        f.write(table2)
        f.close()
        print("Plik zapisano pod nazwą " + nazwa_pliku + "_za.txt")
    elif za_od == "0":
        f = open(nazwa_pliku + "_od.txt", 'w')
        f.write(table2)
        f.close()
        print("Plik zapisano pod nazwą " + nazwa_pliku + "_od.txt")
    else:
        print("Nie udało się zapisać pliku!")


tab = ""
tab, plik_nazwa = wczytaj(tab)
tab, z_od = Cesar(tab)
zapis(tab, plik_nazwa, z_od)
