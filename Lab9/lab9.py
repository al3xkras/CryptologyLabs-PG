import random
from PIL import Image

class Shuffler:
    def __init__(self,key):
        random.seed(23498754298122)
        key_len=len(key)
        self.key_len=key_len
        self.perm=list(range(key_len))
        perm=self.perm
        random.shuffle(perm)
        self.perm_inv=[perm.index(i) for i in range(key_len)]

    def shuffle(self, binary:bytes):
        sh=bytearray()
        if len(binary)<self.key_len:
            binary+=b'\x00'*(self.key_len-len(binary))
        for val in self.perm:
            sh.append(binary[val])
        return bytes(sh)

    def shuffle_inv(self, binary:bytes):
        sh=bytearray()
        if len(binary)<self.key_len:
            binary+=b'\x00'*(self.key_len-len(binary))
        for val in self.perm_inv:
            sh.append(binary[val])
        return bytes(sh)

def binary_op(L:bytes, R:bytes,method):
    assert len(L)==len(R)
    out=bytearray()
    for i in range(len(L)):
        out.append(method(L[i],R[i]))
    return bytes(out)

def xor(L:bytes, R:bytes):
    _add=lambda x,y: x^y
    return binary_op(L,R,_add)

def next_key(key:bytes):
    b_arr=bytearray(key)
    key_n=bytearray()
    for b in b_arr:
        key_n.append((pow(b,2,300)+10)%256)
    return bytes(key_n)

def F(block:bytes, key:bytes):
    res=bytearray()
    i=0
    last_byte=0
    for byte in block:
        res.append((last_byte+byte^key[i]+2*i+pow(i,5,12))%256)
        last_byte=byte
        i=(i+1)%len(key)
    return bytes(res)

def feistel_cipher(binary:bytes, key:bytes,swap=True):
    _len = len(binary)//2
    L0 = binary[0:_len]
    R0 = binary[_len:2 * _len]
    remainder=binary[2*_len:]
    L1 = R0
    R0_f = F(R0, key)
    R1 = xor(L0, R0_f)
    return bytes(bytearray(L1) + bytearray(R1)+bytearray(remainder)) if swap else\
                bytes(bytearray(R1) + bytearray(L1)+bytearray(remainder))

def block_cipher_binary(binary: bytes, key: bytes, decode=False):
    res=binary
    count=8
    key_fun=next_key
    key_lst=[key]
    if decode:
        for _ in range(count-1):
            key=next_key(key)
            key_lst.append(key)
        key_lst=key_lst[::-1]
    for i in range(count):
        k=key if not decode else key_lst[i]
        res=feistel_cipher(res,k,swap=i!=count-1)
        key=key_fun(key)
    return res

def block_cipher_binary_perm(binary, key: bytes, decode=False):
    if not isinstance(binary, bytes):
        binary=str.encode(binary)
    sh=Shuffler(key)
    data= binary[:(len(binary) - len(binary) % len(key))]
    remainder= binary[(len(binary) - len(binary) % len(key)):]
    out=bytearray()
    for i in range(0,len(data),len(key)):
        data_i=data[i:i+len(key)]
        if not decode:
            data_i_proc=block_cipher_binary(data_i,key,decode)
            data_i_proc=sh.shuffle(data_i_proc)
        else:
            data_i_proc = sh.shuffle_inv(data_i)
            data_i_proc = block_cipher_binary(data_i_proc, key, decode)
        out+=data_i_proc
    out=bytes(out)
    if len(remainder)==0:
        return out
    rem=block_cipher_binary_perm(remainder, key[:len(remainder)], decode=decode)
    return out+rem

def block_t(text,key:bytes,decode=False):
    return block_cipher_binary_perm(text,key,decode)

def block_p(image, key: bytes,decode=False):
    if not isinstance(image,bytes):
        image=image.tobytes()
    return block_cipher_binary_perm(image, key,decode)


if __name__ == '__main__':
    b1=bytes(b"some data to encode")
    b2=bytes(b"cryptography in python")

    b_key= b"09jr20d34d"
    print("data",b1)
    encoded=block_cipher_binary(b1,b_key)
    print("enc",encoded)
    decoded=block_cipher_binary(encoded,b_key,decode=True)
    print("dec",decoded)
    decoded = block_cipher_binary(encoded, b"04jr20d34d", decode=True)
    print("dec", decoded)

    print("key:",b_key)
    text=b"text12444t54456htext12444t54456h"
    print("text:",text)
    r=block_t(text, b_key)
    print("encoded text:",r)
    r_=block_t(r, b_key, True)
    print("decoded text:",r_)

    enc_image=False
    if enc_image:
        key=b"23052808289__4t490dp___800129470192f790KHHOdmowdlofihem09__mmmMdx71f07921f701917fca886atextxxd44t5xext1fFlsF4t54456h"
        image=Image.open("image.bmp")
        encoded=block_p(image,key)
        im_enc = Image.frombytes("RGB", (250, 141), encoded)
        im_enc.save("image_encoded.bmp")
        decoded=block_p(encoded,key,decode=True)
        im_dec=Image.frombytes("RGB",(250,141),decoded)
        im_dec.save("image_decoded.bmp")
