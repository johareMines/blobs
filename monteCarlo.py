import random

def monteCarlo(sign, skew=(0.0, 0.0)):
    i, j, k, l = [random.random() for _ in range(4)]

    if sign == "GREATER":
        while i > j:
            i = random.random()
    elif sign == "LESS":
        while i < j:
            i = random.random()

    # Allow negative values
    if k < 0.5:
        i *= -1
    if l < 0.5:
        j *= -1

    i += skew[0]
    j += skew[1]

    return (i, j)