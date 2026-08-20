import math
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def solve_gamblers_fallacy(num_targets: int = 90, sample_size: int = 5) -> list[int]:
    """
    Risolve la fallacia del giocatore d'azzardo disaccoppiando 
    la memoria passata tramite circuiti di cancellazione di fase e QRNG.
    """
    n_qubits = math.ceil(math.log2(num_targets + 1))
    
    # 2 registri: 1 per la memoria storica apparente, 1 per la nuova estrazione
    qc = QuantumCircuit(n_qubits * 2, n_qubits)
    
    reg_history = list(range(0, n_qubits))
    reg_draw = list(range(n_qubits, 2 * n_qubits))
    
    # 1. Simulazione di uno stato iniziale con bias cognitivo (falso ritardo)
    for q in reg_history:
        qc.x(q)
        
    # 2. Distruzione dell'informazione classica / Disaccoppiamento di fase
    #    Applica porte CNOT inverse e Hadamard per annullare l'entanglement con la storia
    for h, d in zip(reg_history, reg_draw):
        qc.cx(h, d)
        qc.reset(h)  # Collasso e azzeramento formale della memoria (Non-memory Markov channel)
        qc.h(d)      # Sovrapposizione uniforme non correlata
        
    # 3. Misurazione proiettiva sul registro di estrazione
    qc.measure(reg_draw, range(n_qubits))
    
    sampler = StatevectorSampler()
    extracted = set()
    
    # Campionamento puro da stato quantistico privo di memoria
    while len(extracted) < sample_size:
        job = sampler.run([(qc,)], shots=100)
        counts = job.result()[0].data.c.get_int_counts()
        
        for val in counts.keys():
            if 1 <= val <= num_targets:
                extracted.add(val)
                if len(extracted) == sample_size:
                    break
                    
    return sorted(list(extracted))


if __name__ == "__main__":
    numeri_estratti = solve_gamblers_fallacy(num_targets=90, sample_size=5)
    print("=" * 70)
    print(" RISOLUZIONE QUANTISTICA DELLA FALLACIA DEL GIOCATORE D'AZZARDO")
    print("=" * 70)
    print(f"Numeri generati privi di memoria temporale: {numeri_estratti}")
    print("Lo stato storico è stato proiettato a |0> e disaccoppiato dal canale.")
    print("=" * 70)