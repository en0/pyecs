from abc import ABC, abstractmethod
from typing import Dict, Set, Iterable, Any, Type, Union, TypeVar, List, Optional
from .entity import Entity


PROVIDER_T = TypeVar("PROVIDER_T")


class ISystem(ABC):

    @abstractmethod
    def update(self) -> None:
        """Update the system."""
        ...


class IEntityManager(ABC):

    @property
    @abstractmethod
    def active_world(self) -> Optional[str]:
        """Gets the currently active world name."""
        ...

    @abstractmethod
    def spawn(self, components: Dict[int, Any] = None) -> int:
        """Add a new entity into the world

        Arguments:
            components: The components that describe the new entity.

        Returns:
            The id of the new entity.
        """
        ...

    @abstractmethod
    def kill(self, entity_id: Union[int, Entity]) -> None:
        """Remove the given entity from the world.

        Arguments:
            entity_id: The entity or it's id.
        """
        ...

    @abstractmethod
    def add_component(self, entity: Union[int, Entity], component_id: int, value: Any) -> None:
        """Add a component to the given entitiy

        Arguments:
            entity: The entity or it's ID.
            component_id: The component flag to add.
            value: The component value to add.
        """
        ...

    @abstractmethod
    def remove_component(self, entity: Union[int, Entity], component: int) -> None:
        """Remove a component from the given entitiy

        Arguments:
            entity: The entity or it's ID.
            component: The component flag to remove.
        """
        ...

    @abstractmethod
    def activate_world(self, name: str) -> None:
        """Activate a world with the given name.

        If a template with the same name exists, the template will be loaded.
        else, a new empty world will be loaded.

        If a world with the given name already exists, it will be clobbered.

        Arguments:
            name: The name of the world.
        """
        ...

    @abstractmethod
    def reactivate_world(self, name: str) -> None:
        """Reactivate the given world.

        If the world has never been activated before, this function will
        call activate_world(name) for you.

        Arguments:
            name: The name of the world to reactivate.
        """
        ...

    @abstractmethod
    def destroy_world(self, name: str) -> None:
        """Destroy the given world.

        Arguments:
            name: The name of the world to destroy.
        """
        ...

    @abstractmethod
    def set_world_template(self, name: str, entities: List[Dict[int, Any]]) -> None:
        """Set a predefined entity list for the given world name.

        The entity list will be copied into the world when activated."

        Arguments:
            name: The name of the world.
            entities: The list of entities.
        """
        ...

    @abstractmethod
    def get_entities(self, component_group: int) -> Iterable[Entity]:
        """Get a group of entities by the given query.

        Only predefined component groups are valid. Be sure the query is installed
        before using.

        Arguments:
            component_group: A entity query.

        Returns:
            An interable of entities that match the given query.
        """
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Optional[Entity]:
        """Get an entity by it's ID

        Arguments:
            entity_id: The id of the desired entity.

        Returns:
            The entity or None.
        """
        ...


class ISystemManager(ABC):

    @abstractmethod
    def install(self, system: ISystem, enabled: bool = True) -> None:
        """Install a new system.

        Arguments:
            system: The new system to be installed.
            enabled: A boolean indicating if the system is enabled.
                     default: True
        """
        ...

    @abstractmethod
    def enable(self, system: Union[Type[ISystem], ISystem]) -> None:
        """Enable the given system.

        Arguments:
            system: The system to be enabled.
        """
        ...

    @abstractmethod
    def disable(self, system: Union[Type[ISystem], ISystem]) -> None:
        """Disable the given system.

        Arguments:
            system: The system to be disabled.
        """
        ...

    @abstractmethod
    def update(self) -> None:
        """Update each installed system."""
        ...


class IGame(ABC):

    @abstractmethod
    def play(self) -> None:
        """Start playing"""
        ...


class IObjectFactory(ABC):
    def get_provider(self, annotation: Type[PROVIDER_T]) -> PROVIDER_T:
        """Get the provider for the given annotation.

        Arguments:
            annotation: The annotation used to activate a provider.
        """
        ...

