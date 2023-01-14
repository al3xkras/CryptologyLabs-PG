
def block_cipher_binary(binary:bytes, key:bytes):

def block_t(text,key:bytes):
    pass

def block_p(image,key:bytes):
    pass

def binary_op(L:bytes, R:bytes,method):
    assert len(L)==len(R)
    out=bytearray()
    for i in range(len(L)):
        out.append(method(L[i],R[i]))
    return bytes(out)

def subs(L:bytes,R:bytes):
    sub=lambda x,y:x-y
    return binary_op(L,R,sub)

def add(L:bytes,R:bytes):
    _add=lambda x,y:y+x
    return binary_op(L,R,_add)

def F(block:bytes, key:bytes):
    res=bytearray()
    i=0
    for byte in block:
        res.append(byte+key[i])
        i=(i+1)%len(key)
    return bytes(res)

def feistel_cipher(binary:bytes, key:bytes):
    _len = len(key)
    L0 = binary[0:_len]
    R0 = binary[_len:2 * _len]
    L1 = R0
    R0_f = F(R0, key)
    R1 = add(L0, R0_f)
    return bytes(bytearray(L1) + bytearray(R1))

if __name__ == '__main__':
    b1=bytes(b"abdbdbdb")
    b2=bytes(b"9sjrnskd")
    m=b1[0]+b2[0]
    print(hex(m),hex(m-b2[0]),hex(b1[0]))

    b1b2=add(b1, b2)
    b2s=subs(b1b2,b1)
    print(b2,b2s)