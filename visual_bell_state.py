#Visual bell state
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

dog_circuit = QuantumCircuit(2)
dog_circuit.h(0)
dog_circuit.cx(0, 1)
dog_circuit.measure_all()

universe = StatevectorSampler()
result = universe.run([dog_circuit], shots=1000000).result()
print(result[0].data.meas.get_counts())

#matplotlib magic
counts = result[0].data.meas.get_counts()
figure = plot_histogram(counts)

plt.show()