import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
st.set_page_config(
    page_title="Toy Hash Collision Structure",
    page_icon="🔬",
    layout="wide"
)

st.title("Toy Hash Collision Structure")
st.subheader("Quantum Simulation Using Simon's Algorithm")

st.write(
    "Explore a 3-bit hidden period using a simulated quantum circuit."
)

st.info(
    "This project uses Qiskit Aer to simulate a quantum circuit "
    "on a classical computer. It does not use real quantum hardware."
)

st.sidebar.header("Simulation Settings")

hidden_period = st.sidebar.selectbox(
    "Select Hidden Period",
    ["001", "010", "011", "100", "101", "110", "111"],
    index=6
)

shots = st.sidebar.selectbox(
    "Number of Shots",
    [256, 512, 1024, 2048, 4096],
    index=2
)

s = int(hidden_period, 2)

def toy_hash(x, period):
    """
    Illustrative toy function:
    f(x) = min(x, x XOR period).

    Inputs x and x XOR period have the same output.
    This is not a cryptographic hash function.
    """
    return min(x, x ^ period)


def get_oracle_rows(period):
    rows = []
    seen = set()

    for x in range(8):
        partner = x ^ period
        pair = tuple(sorted((x, partner)))

        if pair not in seen:
            seen.add(pair)

            rows.append({
                "Input 1": format(pair[0], "03b"),
                "Input 2": format(pair[1], "03b"),
                "Hash Output": format(
                    toy_hash(pair[0], period), "03b"
                )
            })

    return rows


def build_simon_circuit(period):
    """
    Build a 3-input-qubit, 3-output-qubit Simon circuit.

    The oracle performs:
        |x>|y> -> |x>|y XOR f(x)>

    The first register is measured after the final Hadamard gates.
    """

    n = 3
    dimension = 2 ** (2 * n)

    # Construct the reversible oracle as a permutation matrix.
    oracle_matrix = np.zeros(
        (dimension, dimension),
        dtype=complex
    )

    for x in range(2 ** n):
        fx = toy_hash(x, period)

        for y in range(2 ** n):
            input_index = x + (y << n)
            output_y = y ^ fx
            output_index = x + (output_y << n)

            oracle_matrix[output_index, input_index] = 1

    qc = QuantumCircuit(2 * n, n)

    # Step 1: Create a superposition in the input register.
    for q in range(n):
        qc.h(q)

    qc.barrier()

    # Step 2: Apply the reversible oracle.
    qc.unitary(
        Operator(oracle_matrix),
        list(range(2 * n)),
        label="Simon Oracle"
    )

    qc.barrier()

    # Step 3: Apply Hadamard gates to the input register.
    for q in range(n):
        qc.h(q)

    qc.barrier()

    # Step 4: Measure only the input register.
    for q in range(n):
        qc.measure(q, q)

    return qc


# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

qc = build_simon_circuit(s)

simulator = AerSimulator()

compiled_qc = qc
result = simulator.run(
    compiled_qc,
    shots=shots
).result()

counts = result.get_counts()


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Hidden Period", hidden_period)

with col2:
    st.metric("Number of Shots", shots)

with col3:
    st.metric("Measured Outcomes", len(counts))


# --------------------------------------------------
# ORACLE VERIFICATION
# --------------------------------------------------

st.divider()
st.header("1. Oracle Verification")

oracle_df = pd.DataFrame(get_oracle_rows(s))

st.write("Input pairs that produce the same toy hash output:")

st.dataframe(
    oracle_df,
    use_container_width=True,
    hide_index=True
)

oracle_valid = all(
    toy_hash(x, s) == toy_hash(x ^ s, s)
    for x in range(8)
)

if oracle_valid:
    st.success("Oracle mathematical verification passed.")
else:
    st.error("Oracle verification failed.")


# --------------------------------------------------
# MEASUREMENT RESULTS
# --------------------------------------------------

st.divider()
st.header("2. Measurement Results")

st.write(
    "The following table shows the actual bit strings "
    "measured by the Qiskit Aer simulator and their counts."
)

results_df = pd.DataFrame(
    [
        {
            "Measured Outcome": outcome,
            "Number of Shots": count,
            "Probability": count / shots
        }
        for outcome, count in sorted(counts.items())
    ]
)

st.dataframe(
    results_df,
    use_container_width=True,
    hide_index=True
)

st.write(f"**Total measured shots:** {sum(counts.values())}")

if sum(counts.values()) == shots:
    st.success("Measurement counts match the selected number of shots.")
else:
    st.warning("The total count does not match the selected number of shots.")


# --------------------------------------------------
# MEASUREMENT HISTOGRAM
# --------------------------------------------------

st.subheader("Measurement Outcome Distribution")

fig, ax = plt.subplots(figsize=(9, 4))

outcomes = list(sorted(counts.keys()))
values = [counts[outcome] for outcome in outcomes]

ax.bar(outcomes, values)
ax.set_xlabel("Measured Outcome")
ax.set_ylabel("Number of Shots")
ax.set_title("Simon Algorithm Measurement Counts")
ax.grid(axis="y", linestyle="--", alpha=0.4)

st.pyplot(fig)
plt.close(fig)


# --------------------------------------------------
# THEORETICAL VERIFICATION
# --------------------------------------------------

st.divider()
st.header("3. Theoretical Verification")

st.write(
    "Simon's algorithm predicts that each measured outcome "
    "satisfies y · s = 0 modulo 2."
)


def dot_product_mod2(y_string, period_string):
    return sum(
        int(a) * int(b)
        for a, b in zip(y_string, period_string)
    ) % 2


verification_rows = []

for outcome, count in sorted(counts.items()):
    dot_result = dot_product_mod2(outcome, hidden_period)

    verification_rows.append({
        "Measured Outcome": outcome,
        "Number of Shots": count,
        "y · s mod 2": dot_result,
        "Valid": dot_result == 0
    })

verification_df = pd.DataFrame(verification_rows)

st.subheader("Verification Results")

st.dataframe(
    verification_df,
    use_container_width=True,
    hide_index=True
)

all_valid = all(
    row["Valid"] for row in verification_rows
)

if all_valid:
    st.success(
        "All measured outcomes satisfy y · s = 0 mod 2."
    )
else:
    st.error(
        "Some outcomes do not satisfy the expected condition. "
        "Check the circuit and bit ordering."
    )


# --------------------------------------------------
# HIDDEN PERIOD RECOVERY
# --------------------------------------------------

st.divider()
st.header("4. Hidden Period Analysis")

st.write(
    "The simulator's measurement outcomes provide equations "
    "of the form y · s = 0 mod 2. These equations can be used "
    "to identify the hidden period."
)


def recover_period_from_counts(counts):
    """
    Search all nonzero 3-bit candidates.
    A candidate is accepted when it satisfies every
    observed measurement equation and is unique.
    """

    valid_candidates = []

    for candidate in range(1, 8):
        candidate_string = format(candidate, "03b")

        valid = all(
            dot_product_mod2(outcome, candidate_string) == 0
            for outcome in counts
        )

        if valid:
            valid_candidates.append(candidate_string)

    if len(valid_candidates) == 1:
        return valid_candidates[0], valid_candidates

    return None, valid_candidates


recovered_period, candidates = recover_period_from_counts(counts)

if recovered_period is not None:
    st.metric("Recovered Period", recovered_period)

    if recovered_period == hidden_period:
        st.success(
            f"Successfully recovered the hidden period: "
            f"{recovered_period}"
        )
    else:
        st.warning(
            f"The recovered period ({recovered_period}) differs "
            f"from the selected period ({hidden_period})."
        )
else:
    st.warning(
        "The measured equations do not identify one unique "
        "nonzero period. Run more shots or check the simulation."
    )

    st.write("Remaining candidate periods:", candidates)


# --------------------------------------------------
# QUANTUM CIRCUIT
# --------------------------------------------------

st.divider()
st.header("5. Quantum Circuit")

with st.expander("View Quantum Circuit"):
    st.write(
        "The circuit contains three input qubits and three "
        "output qubits. Only the input register is measured."
    )

    st.code(str(qc.draw(output="text")), language="text")
# --------------------------------------------------
# CLASSICAL COLLISION DEMONSTRATION
# --------------------------------------------------

st.divider()
st.header("6. Classical Collision Demonstration")

st.write(
    "Compare two inputs whose toy hash outputs are equal."
)

input1 = st.number_input(
    "Input 1 (0 to 7)",
    min_value=0,
    max_value=7,
    value=1,
    step=1
)

input2 = st.number_input(
    "Input 2 (0 to 7)",
    min_value=0,
    max_value=7,
    value=6,
    step=1
)

hash1 = toy_hash(int(input1), s)
hash2 = toy_hash(int(input2), s)

c1, c2 = st.columns(2)

with c1:
    st.write("**Input 1:**", format(int(input1), "03b"))
    st.write("**Hash Output 1:**", format(hash1, "03b"))

with c2:
    st.write("**Input 2:**", format(int(input2), "03b"))
    st.write("**Hash Output 2:**", format(hash2, "03b"))

if input1 != input2 and hash1 == hash2:
    st.success("Collision verified: distinct inputs have the same output.")
else:
    st.info(
        "These inputs do not demonstrate a collision. "
        "Try two distinct inputs that differ by the hidden period."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built with Python, Streamlit, Qiskit, Qiskit Aer, "
    "NumPy, Pandas and Matplotlib. "
    "This is an educational simulation running on a classical computer."
)