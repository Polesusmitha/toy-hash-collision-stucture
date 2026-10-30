
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from itertools import product

N = 3
HIDDEN_PERIOD = "101"
SHOTS = 1024


def create_simon_circuit():
    # 3 input qubits + 3 output qubits
    # 3 classical bits for input + 3 for output
    qc = QuantumCircuit(6, 6)

    # Step 1: Create superposition
    for qubit in range(N):
        qc.h(qubit)

    # Step 2: Oracle for the hidden period 101
    # f(x) = (x0 XOR x2, x1, 0)
    qc.cx(0, 3)
    qc.cx(2, 3)
    qc.cx(1, 4)

    # Step 3: Measure the output register
    for qubit in range(3):
        qc.measure(qubit + 3, qubit + 3)

    # Step 4: Apply Hadamard to input register
    for qubit in range(N):
        qc.h(qubit)

    # Step 5: Measure the input register
    for qubit in range(N):
        qc.measure(qubit, qubit)

    return qc


def recover_period(outcomes):
    possible = []

    for bits in product("01", repeat=N):
        candidate = "".join(bits)

        if candidate == "000":
            continue

        valid = True

        for y in outcomes:
            dot = sum(
                int(a) * int(b)
                for a, b in zip(candidate, y)
            ) % 2

            if dot != 0:
                valid = False
                break

        if valid:
            possible.append(candidate)

    return possible


if __name__ == "__main__":
    circuit = create_simon_circuit()

    simulator = AerSimulator()
    result = simulator.run(
        circuit,
        shots=SHOTS
    ).result()

    counts = result.get_counts()

    # The rightmost 3 bits are input measurements
    input_counts = {}

    for bitstring, count in counts.items():
        y = bitstring[-3:]
        input_counts[y] = input_counts.get(y, 0) + count

    outcomes = list(input_counts.keys())
    recovered = recover_period(outcomes)

    print("\n================================")
    print(" QUANTUM SIMULATION - SIMON")
    print("================================")

    print("\nHidden period:", HIDDEN_PERIOD)
    print("Number of shots:", SHOTS)

    print("\nMeasurement counts:")
    for y, count in sorted(input_counts.items()):
        print(f"{y}: {count}")

    print("\nChecking theoretical condition:")
    for y in outcomes:
        dot = sum(
            int(a) * int(b)
            for a, b in zip(y, HIDDEN_PERIOD)
        ) % 2

        print(f"y = {y}, y dot s mod 2 = {dot}")

    print("\nPossible hidden periods:", recovered)

    if len(recovered) == 1:
        print("Recovered period:", recovered[0])
        print(
            "Recovery successful:",
            recovered[0] == HIDDEN_PERIOD
        )
    else:
        print("Period not uniquely recovered.")
        print("Run the simulation again.")

    print("\nQuantum circuit:")
    print(circuit.draw(output="text"))
