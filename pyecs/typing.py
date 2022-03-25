from abc import ABC, abstractmethod
from typing import Dict, Set, Iterable, Any


class IEntityManager(ABC):

    @abstractmethod
    def spawn(self, components: Dict[int, Any] = None) -> int:
        ...

    @abstractmethod
    def kill(self, entity_id: int) -> None:
        ...

    @abstractmethod
    def add_component(self, entity_id: int, component_id: int, value: Any) -> None:
        ...

    @abstractmethod
    def create_world(self, name: str) -> None:
        ...

    @abstractmethod
    def activate_world(self, name: str) -> None:
        ...

    @abstractmethod
    def destroy_world(self, name: str) -> None:
        ...

    @abstractmethod
    def get_entities(self, component_group: int) -> Iterable[Dict[int, Any]]:
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Dict[int, Any]:
        ...

