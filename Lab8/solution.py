import algorytm
from PIL import Image
import numpy as np

def colors_equal(px1,px2,color_i=0):
    for i in range(len(px1)):
        row1=px1[0]
        row2=px2[0]
        for j in range(len(row1)):
            if not row1[j][color_i]==row2[j][color_i]:
                return False
    return True

def find_key(first_line_plain, first_line_encoded):
    fp,fe=first_line_plain,first_line_encoded
    key_length=12
    encode = lambda image, _key: algorytm.blokowy(image, image.load(), None, _key, 1)

    b2 = np.asarray(fe)
    keys=[None,None,None]
    for k in range(pow(2,key_length)):
        key_bin=str(bin(k))[2:]
        if len(key_bin)<key_length:
            key_bin+="0"*(key_length-len(key_bin))
        b1=np.asarray(encode(fp.copy(),key_bin))
        k=0
        for i in range(len(keys)):
            if colors_equal(b1, b2, i):
                k+=1
                keys[i]=key_bin
        if k==3:
            return keys[0]
    print("key not found for >=1 color.")
    return keys

if __name__ == '__main__':
    fname_plain=None#input("file name (plain): ")
    fname_cipher=None#input("file name (cipher): ")

    fname_plain = fname_plain if fname_plain else "im1_partdec.bmp"
    fname_cipher = fname_cipher if fname_cipher else "im1.bmp"

    plain = algorytm.read_image(fname_plain)[0]
    cipher = algorytm.read_image(fname_cipher)[0]
    first_line_plain=Image.fromarray(np.array(
        [np.asarray(plain)[0]]
    ))

    first_line_encoded=Image.fromarray(np.array(
        [np.asarray(cipher)[0]]
    ))

    key = find_key(first_line_plain,first_line_encoded)
    print("possible key: ",key)
