from typing import Dict, Set, Iterable, Any, NamedTuple, List, Union, Optional
from copy import deepcopy
from math import log
from .typing import IEntityManager
from .entity import Entity


class EntityManagerOpts(NamedTuple):
    component_groups: Set[int]


class EntityCollection:

    def add_entity(self, entity: Entity):
        if entity.identity in self._entities:
            raise RuntimeError("Entity ID Collision. Abort!")
        self._entities[entity.identity] = entity
        self._reverse_groups[entity.identity] = set()
        group_mask = 0
        for component_id in entity.keys():
            group_mask |= component_id
        for group in self._groups:
            if (group & group_mask) == group:
                self._groups[group].add(entity.identity)
                self._reverse_groups[entity.identity].add(group)

    def remove_entity(self, entity_id: int) -> None:
        for group in self._reverse_groups[entity_id]:
            self._groups[group].remove(entity_id)
        del self._reverse_groups[entity_id]
        del self._entities[entity_id]

    def add_component(self, entity_id: int, component_id: int, data: Any) -> None:
        current = self.get_entity(entity_id)
        current[component_id] = data
        self.remove_entity(entity_id)
        self.add_entity(current)

    def remove_component(self, entity_id: int, component_id: int) -> None:
        current = self.get_entity(entity_id)
        del current[component_id]
        self.remove_entity(entity_id)
        self.add_entity(current)

    def get_entities(self, component_group: int) -> Iterable[Entity]:
        # copy the set so the set cannot be modified during iteration
        for _id in self._groups.get(component_group, []).copy():
            if _id in self._entities:
                yield self._entities[_id]

    def get_entity(self, entity_id: int) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def __init__(self, groups: Set[int]):
        self._entities: Dict[int, dict] = {}
        self._groups: Dict[int, Set[int]] = {g: set() for g in groups}
        self._reverse_groups: Dict[int, Set[int]] = {}


class EntityManager(IEntityManager):

    @property
    def active_world(self) -> Optional[str]:
        return self._active_world_name

    def activate_world(self, name: str) -> None:
        self._active_world_name = name
        self._worlds[name] = EntityCollection(self._groups)
        self._active_world = self._worlds[name]
        for entity in self._templates.get(name, []):
            self.spawn(deepcopy(entity))

    def reactivate_world(self, name: str) -> None:
        if name not in self._worlds:
            self.activate_world(name)
        else:
            self._active_world_name = name
            self._active_world = self._worlds[name]

    def destroy_world(self, name: str) -> None:
        del self._worlds[name]

    def set_world_template(self, name: str, entities: List[Dict[int, Any]]):
        self._templates[name] = entities

    def spawn(self, components: Dict[int, Any] = None) -> int:
        entity = Entity(components)
        entity.identity = self._get_next_entity_id()
        self._active_world.add_entity(entity)
        return entity.identity

    def kill(self, entity: Union[int, Entity]) -> None:
        entity_id = entity.identity if isinstance(entity, Entity) else entity
        self._active_world.remove_entity(entity_id)

    def add_component(self, entity: Union[int, Entity], component_id: int, value: Any) -> None:
        entity_id = entity.identity if isinstance(entity, Entity) else entity
        self._active_world.add_component(entity_id, component_id, value)

    def remove_component(self, entity: Union[int, Entity], component: int) -> None:
        entity_id = entity.identity if isinstance(entity, Entity) else entity
        self._active_world.remove_component(entity_id, component)

    def get_entities(self, component_group: int) -> Iterable[Entity]:
        return self._active_world.get_entities(component_group)

    def get_entity(self, entity_id: int) -> Optional[Entity]:
        return self._active_world.get_entity(entity_id)

    def _get_next_entity_id(self) -> int:
        self._counter += 1
        return self._counter

    def __init__(self, opts: EntityManagerOpts) -> None:
        component_groups = opts.component_groups.copy()
        self._counter = 0
        self._active_world: EntityCollection = EntityCollection(component_groups)
        self._worlds: Dict[str, EntityCollection] = {}
        self._groups: Set[int] = component_groups
        self._templates: Dict[str,List[Dict[int, Any]]] = {}
        self._active_world_name = None
