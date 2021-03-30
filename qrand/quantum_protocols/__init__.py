##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: March 28, 2021
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
from typing import Literal, Optional

from ..quantum_platforms import QuantumPlatform
from ..validation_strategies import ValidationStrategy

###############################################################################
## EXPOSE IMPLEMENTATIONS
###############################################################################
from ._protocol_resutls import ProtocolResult, SimpleResult


###############################################################################
## QUANTUM PROTOCOL INTERFACE (STRATEGY AND DECORATOR)
###############################################################################
class QuantumProtocol(ABC):
    ############################ STRATEGY PATTERN ############################
    @abstractmethod
    def run(self, platform: QuantumPlatform) -> Optional[ProtocolResult]:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass

    ############################ DECORATOR PATTERN ############################
    @abstractmethod
    def validate(self, result: ProtocolResult) -> bool:
        pass

    @property
    @abstractmethod
    def base_protocol(self) -> Optional[QuantumProtocol]:  # noqa: F821
        pass


###############################################################################
## PROTOCOL STRATEGY INTERFACE
###############################################################################
class ProtocolStrategy(QuantumProtocol):
    ############################ STRATEGY PATTERN ############################
    @abstractmethod
    def run(self, platform: QuantumPlatform) -> Optional[ProtocolResult]:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass

    ############################ DECORATOR PATTERN ############################
    def validate(self, result: ProtocolResult) -> Literal[False]:
        return False

    @property
    def base_protocol(self) -> Literal[None]:
        return None


###############################################################################
## VALIDATION DECORATOR
###############################################################################
class ValidationDecorator(QuantumProtocol):
    def __init__(
        self,
        base_protocol: QuantumProtocol,
        validation_strategy: ValidationStrategy,
    ) -> None:
        self.base_protocol: QuantumProtocol = base_protocol
        self._validation_strategy: ValidationStrategy = validation_strategy

    ############################ STRATEGY PATTERN ############################
    def run(self, platform: QuantumPlatform) -> Optional[ProtocolResult]:
        result: Optional[ProtocolResult] = self.base_protocol.run(platform)
        return result if result is None or self.validate(result) else None

    def verify(self) -> bool:
        return self.base_protocol.verify()

    ############################ DECORATOR PATTERN ############################
    def validate(self, result: ProtocolResult) -> bool:
        validation_token: str = result.validation_token
        validation: bool = self._validation_strategy.validate(validation_token)
        if self.base_protocol.base_protocol is None:
            return validation
        return validation and self.base_protocol.validate(result)
