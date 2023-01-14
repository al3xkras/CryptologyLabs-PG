import random
random.seed(105928893)

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
    for byte in block:
        res.append((byte^key[i]+i+pow(i,5,12))%256)
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

def swap_lr(binary:bytes):
    _len = len(binary)
    # return bytes(bytearray(binary[_len:2 * _len]) + bytearray(binary[0:_len]))
    return binary

def block_cipher_binary(binary: bytes, key: bytes, decode=False):
    res=binary
    count=17
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
        print(k)
        key=key_fun(key)
    if decode:
        return swap_lr(res)
    return res

def block_t(text: str, key: bytes):
    return block_cipher_binary(bytes(text), key)

def block_p(image, key: bytes):
    return block_cipher_binary(bytes(image), key)

if __name__ == '__main__':
    b1=bytes(b"some data to encode")
    b2=bytes(b"cryptography in python")

    b_key= b"09jr20d34d"
    print("data",b1)
    encoded=block_cipher_binary(b1,b_key)
    print("enc",encoded)
    decoded=block_cipher_binary(encoded,b_key,decode=True)
    print("dec",decoded)
    decoded = block_cipher_binary(encoded, b"04jr22d34d", decode=True)
    print("dec", decoded)