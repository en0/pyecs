import pygame
from pyioc3 import ScopeEnum
from abc import ABC, abstractmethod
from typing import Union, TypeVar, Type, Iterable, Dict, Tuple, Any, Optional, Callable, NamedTuple


class ICommand(ABC):

    @abstractmethod
    def execute(self, event: pygame.event.Event):
        ...


class CommandBinding(NamedTuple):
    event_type: int
    command: ICommand
    parameters: Dict[str, Any]


COMPONENT_T = TypeVar("COMPONENT_T", bound=Dict)
Entity = Dict[Type[COMPONENT_T], COMPONENT_T]


class IScene(ABC):

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def teardown(self) -> None:
        ...

    @abstractmethod
    def spawn(self, preset: Entity) -> int:
        ...

    @abstractmethod
    def kill(self, entity_id: int) -> None:
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Entity:
        ...

    @abstractmethod
    def get_entities(self, component_t: Type[COMPONENT_T]) -> Iterable[Entity]:
        ...

    @abstractmethod
    def get_commands(self, event_type: int) -> Iterable[CommandBinding]:
        ...

    @abstractmethod
    def install(self, event_type: int, command: ICommand, **props) -> int:
        ...

    @abstractmethod
    def uninstall(self, handle: int) -> None:
        ...

    @abstractmethod
    def update(self, frame_delay: float) -> None:
        ...


class ISystem(ABC):

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def teardown(self) -> None:
        ...

    @abstractmethod
    def update(self, scene: IScene, frame_delay: float) -> None:
        ...


PROVIDER_T = TypeVar("PROVIDER_T")
ActivatorDelegate = Callable[[PROVIDER_T], PROVIDER_T]


class IGameContainer(ABC):

    @abstractmethod
    def add_provider(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate: Optional[ActivatorDelegate] = None,
    ) -> None: ...

    @abstractmethod
    def add_constant(
        self,
        annotation: Type,
        value: Any,
    ) -> None: ...

    @abstractmethod
    def get_provider(
        self,
        provider: Type[PROVIDER_T]
    ) -> PROVIDER_T: ...


class IGame(ABC):

    @abstractmethod
    def setup(self, container: IGameContainer) -> None:
        ...

    @abstractmethod
    def teardown(self) -> None:
        ...

    @abstractmethod
    def run(self) -> None:
        ...

    @abstractmethod
    def push_scene(self, scene_t: Type[Union[IScene, str]]) -> None:
        ...

    @abstractmethod
    def pop_scene(self) -> IScene:
        ...

