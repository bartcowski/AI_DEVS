double = [x**2 for x in [0, 5, 7, 9]]
print(double)

tri = [x**3 for x in range(1, 5)]
print(tri)

odd = [x for x in range(25) if x % 2 != 0]
print(odd)

mult = [x * y for x in [1, 3, 5] for y in [11, 54, 4]]
print(mult)

multObj = [{'x': x, 'y': y, 'result': x * y} for x in [1, 3, 5] for y in [11, 54, 4]]
print(multObj)

conditional = ['TRES' if x % 3 == 0 else 'NADA' for x in range(11)]
print(conditional)