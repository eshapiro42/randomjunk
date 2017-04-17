import random, math

def miller_rabin (n, k): # n is the number to be tested for primality
                         # k is the number of tries
    # Test that n > 3
    if n <= 3:
        raise ValueError("n must be greater than 3")
    # Test for obvious non-primes
    for i in range (2, min (n, 10)):
        if n % i == 0:
            return False
    # Write (n - 1) as (d * 2^r) with d odd by factoring powers of 2 from (n - 1)
    m = n - 1
    r = 0
    while m % 2 == 0: # while m is even
        m //= 2	# divide m by 2
        r +=  1	# increment r
    d = m
    # Attempt k times to show that n is not prime
    for i in range (k):
        a = random.randint (2, n - 2)
        x = pow (a, d, n)
        if x != 1:
            j = 0
            while x != (n - 1):
                if j == r - 1:
                    return False
                else:
                    j += 1
                    x = pow (x, 2, n)
    return True

def inverse (a, n): # a is the number whose inverse we wish to find
                    # n is the modulus
    for i in range (1, n):
        if (i * a) % n == 1:
            return i

def rsa (length):
    # Generate two large prime numbers, p and q
    p = random.randint (10 ** (length - 1), 10 ** length - 1)
    if p % 2 == 0:
        p += 1
    while miller_rabin (p, 64) == False:
        p += 2
    q = random.randint (10 ** (length - 1), 10 ** length - 1)
    if q % 2 == 0:
        q += 1
    while miller_rabin (q, 64) == False:
        q += 2
    # Calculate the modulus, n
    n = p * q
    # Calculate the totient of n, phi
    phi = (p - 1) * (q - 1)
    # Generate the public key
    e = 65537
    while math.gcd(e, phi) != 1:
        e += 2
        while miller_rabin(e, 64) == False:
            e += 2
    # Generate the private key
    d = inverse (e, phi)
    # Return results
    return [e, d, n]            
