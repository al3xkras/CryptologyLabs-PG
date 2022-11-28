from random import randint

def is_prime_sqrt(p):
    pass

def is_prime_miller_rabin(p):
    pass

def fermat_test(n, k):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(k):
        a = randint(1, n - 1)
        if pow(a, n - 1) % n != 1:
            return False
    return True

if __name__ == '__main__':
    print(fermat_test(15,10))
