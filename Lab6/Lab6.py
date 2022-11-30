from random import randint

def is_prime_sqrt(p):
    pass

def is_prime_miller_rabin(n, k):
    """
    Input: n > 2, an odd integer to be tested for primality;
       k, a parameter that determines the accuracy of the test
    Output: composite if n is composite, otherwise probably prime
    write n − 1 as 2s·d with d odd by factoring powers of 2 from n − 1
    LOOP: repeat k times:
       pick a randomly in the range [2, n − 1]
       x ← a d mod n
       if x = 1 or x = n − 1 then do next LOOP
       repeat s − 1 times:
          x ← x 2 mod n
          if x = 1 then return composite
          if x = n − 1 then do next LOOP
       return composite
    return probably prime
    """
    if not n&1 or n==1:
        return False
    s=1
    d=n-1
    while not d&1:
        s*=2
        d//=2
    for i in range(k):
        a = randint(2,n-1)
        x = pow(a,d,n)
        if x==1 or x==n-1:
            continue
        for j in range(s-1):
            x = pow(x,2,n)
            if x==1:
                return False
            if x==n-1:
                break
        if x==n-1:
            continue
        return False
    return True

def fermat_test(n, k):
    pass

if __name__ == '__main__':
    def test_miller_rabin():
        assert is_prime_miller_rabin(0, 2) is False
        assert is_prime_miller_rabin(1, 2) is False
        assert is_prime_miller_rabin(2, 2) is False
        assert is_prime_miller_rabin(3, 20) is True
        assert is_prime_miller_rabin(10, 5) is False
        assert is_prime_miller_rabin(101, 20) is True
        assert is_prime_miller_rabin(1001, 30) is False
        assert is_prime_miller_rabin(4547337172376300111955330758342147474062293202868155909489,30000) is True
        assert is_prime_miller_rabin(4547337172376300111955330758342147474062293202868155909393, 30000) is False
    test_miller_rabin()
    """
    Conclusions: the Miller-Rabin test is a probabilistic primality test, that
        allows to determine if a given number is prime with a high probability.
        It is much faster in comparison to the non-probabilistic square root primality test,
        and the accuracy of the test results can be specified and changed.
        This test excels in the primality analysis of large numbers (e.g. >1e6),
        because of the reduced execution time and resource consumption,
        however its results are not definite with a probability of 100%.
        Nevertheless, the Miller-Rabin test is widely known and used. It is considered a classic
        primality test.
    """

