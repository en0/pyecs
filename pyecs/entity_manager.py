from typing import Dict, Set, Iterable, Any, List, Optional
from math import log
from .typing import IEntityManager


class EntityCollection:

    def add_entity(self, entity_id: int, components: Dict[int, Any] = None):
        if entity_id in self._entities:
            raise RuntimeError("Entity Collision. Abort!")
        self._entities[entity_id] = components
        self._reverse_groups[entity_id] = set()
        group_mask = 0
        for component_id in components.keys():
            group_mask |= component_id
        for group in self._groups:
            if (group & group_mask) == group:
                self._groups[group].add(entity_id)
                self._reverse_groups[entity_id].add(group)

    def remove_entity(self, entity_id: int) -> None:
        for group in self._reverse_groups[entity_id]:
            self._groups[group].remove(entity_id)
        del self._reverse_groups[entity_id]
        del self._entities[entity_id]

    def add_component(self, entity_id: int, component_id: int, data: Any) -> None:
        current = self.get_entity(entity_id)
        current[component_id] = data
        self.remove_entity(entity_id)
        self.add_entity(entity_id, current)

    def remove_component(self, entity_id: int, component_id: int) -> None:
        current = self.get_entity(entity_id)
        del current[component_id]
        self.remove_entity(entity_id)
        self.add_entity(entity_id, current)

    def get_entities(self, component_group: int) -> Iterable[Dict[int, Any]]:
        # copy the set so the set cannot be modified during iteration
        for _id in self._groups.get(component_group, []).copy():
            if _id in self._entities:
                yield self._entities[_id]

    def get_entity(self, entity_id: int) -> Dict[int, Any]:
        return self._entities[entity_id]

    def __init__(self, groups: Set[int]):
        self._entities: Dict[int, dict] = {}
        self._groups: Dict[int, Set[int]] = {g: set() for g in groups}
        self._reverse_groups: Dict[int, Set[int]] = {}


class EntityManager(IEntityManager):

    def create_world(self, name: str) -> None:
        self._worlds[name] = EntityCollection(self._groups)

    def activate_world(self, name: str) -> None:
        self._active_world = self._worlds[name]

    def destroy_world(self, name: str) -> None:
        del self._worlds[name]

    def spawn(self, components: Dict[int, Any] = None) -> int:
        entity_id = self._get_next_entity_id()
        self._active_world.add_entity(entity_id, components)
        return entity_id

    def kill(self, entity_id: int) -> None:
        self._active_world.remove_entity(entity_id)

    def add_component(self, entity_id: int, component_id: int, value: Any) -> None:
        self._active_world.add_component(entity_id, component_id, value)

    def remove_component(self, entity_id: int, component: int) -> None:
        self._active_world.remove_component(entity_id, component)

    def get_entities(self, component_group: int) -> Iterable[Dict[int, Any]]:
        return self._active_world.get_entities(component_group)

    def get_entity(self, entity_id: int) -> Dict[int, Any]:
        return self._active_world.get_entity(entity_id)

    def _get_next_entity_id(self) -> int:
        self._counter += 1
        return self._counter

    def __init__(self, component_groups: Set[int], worlds: Set[str] = None) -> None:
        self._counter = 0
        self._active_world: Optional[EntityCollection] = None
        self._worlds: Dict[str, EntityCollection] = {}
        self._groups: Set[int] = component_groups.copy()
        for name in (worlds or []):
            self.create_world(name)
