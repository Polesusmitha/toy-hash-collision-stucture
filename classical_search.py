
# Classical Collision Search
# Project: 3-Bit Hash Function

def classical_collision_search(hash_table):
    seen = {}

    for x, hash_value in sorted(hash_table.items()):
        if hash_value in seen:
            previous_x = seen[hash_value]

            if previous_x != x:
                return previous_x, x, hash_value

        seen[hash_value] = x

    return None


if __name__ == "__main__":
    print("CLASSICAL COLLISION SEARCH")
    hidden_period = input("Enter the 3-bit hidden period: ").strip()

    if (
        len(hidden_period) != 3
        or any(bit not in "01" for bit in hidden_period)
        or hidden_period == "000"
    ):
        print("Invalid input! Enter a valid 3-bit binary number.")
        raise SystemExit

    # Build the same hash table used in Simon's simulation
    period = int(hidden_period, 2)
    hash_table = {}
    output = 0

    for x in range(8):
        paired_x = x ^ period

        if x not in hash_table and paired_x not in hash_table:
            hash_value = format(output, "03b")
            hash_table[x] = hash_value
            hash_table[paired_x] = hash_value
            output += 1

    collision = classical_collision_search(hash_table)

    if collision:
        x1, x2, value = collision

        print("\nCollision found!")
        print("Input 1:", format(x1, "03b"))
        print("Input 2:", format(x2, "03b"))
        print("Common hash value:", value)
        print("XOR of inputs:", format(x1 ^ x2, "03b"))
        print("Entered hidden period:", hidden_period)
        print("Collision matches period:", (x1 ^ x2) == period)
    else:
        print("No collision found.")
