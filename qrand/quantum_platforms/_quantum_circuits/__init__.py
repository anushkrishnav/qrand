##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: March 29, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from abc import ABC, abstractmethod

###############################################################################
## EXPOSE IMPLEMENTATIONS
###############################################################################
from ._cirq_circuit import CirqCircuit
from ._qiskit_circuit import QiskitCircuit
from ._qsharp_circuit import QsharpCircuit


###############################################################################
## QUANTUM CIRCUIT INTERFACE (ADAPTER)
###############################################################################
class QuantumCircuit(ABC):
    @property
    @abstractmethod
    def num_qubits(self) -> int:
        pass

    @abstractmethod
    def h(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def cx(self, control_qubit: int, target_qubit: int) -> None:
        pass

    @abstractmethod
    def measure(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def extract_base_circuit(self):
        pass
