# AUTHOR : vietcv
# LINK : https://codelearn.io/training/1791
def check_prime(n):
    if n < 2:
        return False
    for i in range(2,int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
def extract(n, lis = []):
    if n == 0:
        return 10
    while n >= 10:
        for i in range(9, 1, -1):
            if n % i == 0:
                n = int(n/i)
                lis.append(str(i))
                return extract(n, lis)
        return False
    return  str(n) + "".join(lis[::-1])
def digitsproduct(product):
    if check_prime(product):
        return -1
    result = extract(product)
    return int(result)