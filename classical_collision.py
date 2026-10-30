
print("CLASSICAL COLLISION SEARCH")
print("---------------------------")

s = 0b111

x1 = 0b011
x2 = 0b100

# Toy function: inputs related by XOR with s
# produce the same output
def toy_hash(x):
    return min(x, x ^ s)

h1 = toy_hash(x1)
h2 = toy_hash(x2)

print("Hidden Period:", format(s, "03b"))
print("Input 1:", format(x1, "03b"))
print("Input 2:", format(x2, "03b"))
print("Hash Output 1:", format(h1, "03b"))
print("Hash Output 2:", format(h2, "03b"))
print("XOR of Inputs:", format(x1 ^ x2, "03b"))
print("Collision Verified:", h1 == h2 and (x1 ^ x2) == s)
