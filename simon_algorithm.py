
from itertools import product


def parity(value):
    return value.bit_count() % 2


def simulate_simon(period):
    s = int(period, 2)

    print("\n--- Simon's Algorithm Simulation ---")
    print("Hidden period:", period)

    # Generate independent measurement equations y · s = 0
    outcomes = [
        format(y, "03b")
        for y in range(1, 8)
        if parity(y & s) == 0
    ]

    print("Measurement outcomes:", outcomes)

    # Find non-zero periods consistent with the outcomes
    candidates = []

    for bits in product("01", repeat=3):
        candidate = "".join(bits)

        if candidate == "000":
            continue

        if all(
            sum(int(a) * int(b)
                for a, b in zip(candidate, y)) % 2 == 0
            for y in outcomes
        ):
            candidates.append(candidate)

    print("Possible periods:", candidates)

    if candidates == [period]:
        print("Successfully recovered:", period)
    else:
        print("Could not uniquely recover the period.")


if __name__ == "__main__":
    print("Simon's Algorithm - Classical Demonstration")
    period = input("Enter a 3-bit hidden period (e.g. 111): ").strip()

    if len(period) == 3 and set(period) <= {"0", "1"} and period != "000":
        simulate_simon(period)
    else:
        print("Invalid input! Enter a non-zero 3-bit binary string.")
