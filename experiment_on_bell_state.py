# Experiments

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

parrot_circuit = QuantumCircuit(3)
parrot_circuit.h(0)
parrot_circuit.cx(0, 1)
parrot_circuit.cx(1, 2)
parrot_circuit.x(1)
parrot_circuit.measure_all()

universe = StatevectorSampler()
result = universe.run([parrot_circuit], shots=1084).result()

print(result[0].data.meas.get_counts())