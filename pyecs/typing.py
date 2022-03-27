from abc import ABC, abstractmethod
from typing import Dict, Set, Iterable, Any, Type, Union, TypeVar, List, Optional
from .entity import Entity


PROVIDER_T = TypeVar("PROVIDER_T")


class ISystem(ABC):

    @abstractmethod
    def update(self, frame_delta: float) -> None:
        ...


class IEntityManager(ABC):

    @abstractmethod
    def spawn(self, components: Dict[int, Any] = None) -> int:
        ...

    @abstractmethod
    def kill(self, entity_id: Union[int, Entity]) -> None:
        ...

    @abstractmethod
    def add_component(self, entity_id: int, component_id: int, value: Any) -> None:
        ...

    @abstractmethod
    def activate_world(self, name: str) -> None:
        ...

    @abstractmethod
    def reactivate_world(self, name: str) -> None:
        ...

    @abstractmethod
    def destroy_world(self, name: str) -> None:
        ...

    @abstractmethod
    def set_world_template(self, name: str, entities: List[Dict[int, Any]]):
        ...

    @abstractmethod
    def get_entities(self, component_group: int) -> Iterable[Entity]:
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Optional[Entity]:
        ...


class ISystemManager(ABC):

    @abstractmethod
    def install(self, system: ISystem, enabled: bool = True) -> None:
        ...

    @abstractmethod
    def enable(self, system: Union[Type[ISystem], ISystem]) -> None:
        ...

    @abstractmethod
    def disable(self, system: Union[Type[ISystem], ISystem]) -> None:
        ...

    @abstractmethod
    def update(self, frame_delta: float) -> None:
        ...


class IGame(ABC):

    @abstractmethod
    def play(self):
        ...


class IObjectFactory(ABC):
    def get_provider(self, annotation: Type[PROVIDER_T]) -> PROVIDER_T:
        ...

