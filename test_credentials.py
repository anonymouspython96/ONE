from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# 1. Service (using the saved credentials)
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# 2. Choose a real backend
backend = service.least_busy(simulator=False, operational=True, min_num_qubits=2)
print("Backend choosed:", backend.name, "- qubit:", backend.num_qubits)

# 3. Circuit Bell of 2 qubit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print("\nOriginal circuit: ")
print(qc.draw())

# 4. Optimization of the circuit for the backend
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

print("\nCircuit transformed for the backend:")
print(isa_circuit.draw())

# 5. Execute with Sampler
sampler = Sampler(mode=backend)
sampler.options.default_shots = 1024

job = sampler.run([isa_circuit])
print("\nJob ID:", job.job_id())
print("Status of the job:", job.status())

# 6. Wait for the counts and print the results
result = job.result()
counts = result[0].data.meas.get_counts()
print("\nResults (counts):")
print(counts)

print("\nIf you see only '00' and '11', the bell circuit was executed correctly on hardware.")