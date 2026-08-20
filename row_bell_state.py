#Bell state 2 qubits

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def BellState(s) :

    cat_circuit = QuantumCircuit(2)
    cat_circuit.h(0) #Hadamard portal (the flipper if we think about a coin)
    cat_circuit.cx(0, 1) #cx(control, target) is controlled-not 
    cat_circuit.measure_all() #measures the qubits in the circuit

    universe = StatevectorSampler() #the simulator because we don't have real quantum computer
    result = universe.run([cat_circuit], shots=s).result()
    '''
    run(...) = starts the job and returns the job OBJECT. #start the experiment
    result() = waits for the job to finish and gives you the result OBJECT containing all the data
    (counts, metadata, ...) #give me the final result
    '''

    print(result[0].data.meas.get_counts())

    '''
    result[0] = you run a list of circuits [cat_circuit] (one circuit)
                The result contains results for each circuit in that list.
                #result[0] the result for the first(and only) circuit in the list
                #result[1] the result for the second(and only) circuit in the list
                #result[0], result[1] are the results for two circuits

    .data() = result[0].data() is an object that holds all the mesured data for that circuit.
                It groups different kinds of data (measurements, probabilities, etc...)

    .meas() = stands for mesurement.
                It refers specifically to the classical measurement results 
                (the 0 / 1 outcomes for each qubit)

    So result[0].data().meas(): means "the measurement data for the first circuit".

    .get_counts() = returns a dictionary with how many times each outcome appeard across all shots. 

    '''

BellState(30463311)