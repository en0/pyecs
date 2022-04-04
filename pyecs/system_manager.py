from typing import Type, List, Set, Dict, Union
from .typing import ISystemManager, ISystem


class SystemManager(ISystemManager):

    def install(self, system: ISystem, enabled: bool = True) -> None:
        self._sys_by_type[type(system)] = system
        self._systems.append(system)
        if not enabled:
            self._disabled.add(system)

    def enable(self, system: Union[Type[ISystem], ISystem]) -> None:
        if not isinstance(system, ISystem):
            system = self._sys_by_type[system]
        if system in self._disabled:
            self._disabled.remove(system)

    def disable(self, system: Union[Type[ISystem], ISystem]) -> None:
        if not isinstance(system, ISystem):
            system = self._sys_by_type[system]
        self._disabled.add(system)

    def update(self) -> None:
        for system in self._systems:
            if system not in self._disabled:
                system.update()

    def __init__(self):
        self._systems: List[ISystem] = []
        self._disabled: Set[ISystem] = set()
        self._sys_by_type: Dict[Type[ISystem], ISystem] = {}

