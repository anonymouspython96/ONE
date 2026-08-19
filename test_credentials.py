from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# 1. Servizio (usa le credenziali già salvate)
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# 2. Scegli un backend reale (il meno occupato, almeno 2 qubit)
backend = service.least_busy(simulator=False, operational=True, min_num_qubits=2)
print("Backend scelto:", backend.name, "- qubit:", backend.num_qubits)

# 3. Circuito Bell a 2 qubit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

print("\nCircuito originale:")
print(qc.draw())

# 4. Ottimizza il circuito per il backend
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

print("\nCircuito trasformato per il backend:")
print(isa_circuit.draw())

# 5. Esegui con Sampler
sampler = Sampler(mode=backend)
sampler.options.default_shots = 1024

job = sampler.run([isa_circuit])
print("\nJob ID:", job.job_id())
print("Stato del job:", job.status())

# 6. Attendi il risultato e stampa i counts
result = job.result()
counts = result[0].data.meas.get_counts()
print("\nRisultati (counts):")
print(counts)

print("\nSe vedi prevalentemente '00' e '11', il circuito Bell è stato eseguito correttamente su hardware.")