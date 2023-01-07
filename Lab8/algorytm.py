def plus(a,b):
    n=len(a)
    wynik=""
    for i in range(n):
        wynik+=str(( int(a[i])+int(b[i]) ) % 2)
    return wynik

def f(a,klucz):
    n=len(klucz)
    k=int(klucz,2)

    wynik=""
    for i in range(n):
        wynik+=str(( int(a[i])+k+int(klucz[i])) % 2)
    return wynik

def feistel(dane,klucz):
        dlugosc=len(klucz)
        L0=dane[0:dlugosc]
        R0=dane[dlugosc:2*dlugosc]
        L1=R0
        fei=f(R0,klucz)
        R1=plus(L0,fei)
        return L1+R1
from PIL import Image

def read_image(fname):
    img = Image.open(fname)
    pixels = img.load()
    return img,pixels

def blokowy(img,pixels,nazwa,klucz,p,write=False,log=False):
    dlugosc=len(klucz)

    lista="" 
    for i in range(img.size[0]):    #szerokosc
        for j in range(img.size[1]): #wysokosc
            for k in range(3):
                pixel=bin(pixels[i,j][k])
                pixel=pixel[2:]
                pixel=pixel.zfill(8)
                lista+=pixel
    if log:
        print("Obraz został zamieniony na ciąg bitów")

    #Feistel
    lista2=""
    for i in range(0,len(lista),2*dlugosc):
        blok=lista[i:i+2*dlugosc]
        if p==0:
            blok=blok[dlugosc:2*dlugosc]+blok[0:dlugosc]    
        blok=feistel(blok,klucz) # 1 iteracja
        blok=feistel(blok,klucz) # 2 iteracja
        if p==0:
            blok=blok[dlugosc:2*dlugosc]+blok[0:dlugosc]
        lista2+=blok
        
    if p==1 and log:
        print("Szyfrowanie zakończone")
    elif p==0 and log:
        print("Deszyfrowanie zakończone")

    #zapis do pliku po pikselu
    for i in range(img.size[0]):    #szerokosc
        for j in range(img.size[1]): #wysokosc
            pixel=lista2[0:24]
            lista2=lista2[24:]
            pixels[i,j]=(int(pixel[0:8],2),int(pixel[8:16],2),int(pixel[16:24],2),2)
##    img.show()
    if not write:
        return img
    if p==1:
        nazwa2=nazwa[:-4]+"_"+klucz+".bmp"
    elif p==0:
        nazwa2=nazwa[:-4]+"_"+klucz+"1.bmp"
    img.save(nazwa2)
    if log:
        print("Obraz wynikowy zostal zapisany jako " + nazwa2)
    return img

if __name__ == '__main__':
    klucz="110101000001" #klucz dlugosci 12
    name="im1.bmp"
    im,pix=read_image(name)
    blokowy(im,pix,name,klucz,0,write=True,log=True) # 0 oznacza probe deszyfrowania


