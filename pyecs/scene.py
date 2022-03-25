import pygame
from typing import Dict, List, Iterable, Deque, Tuple, Type
from collections import deque
from .typing import IScene, CommandBinding, ICommand, IGame, Entity, COMPONENT_T
from .commands import DelegatedCommand


class Scene(IScene):

    @property
    def game(self) -> IGame:
        return self._game

    def setup(self) -> None:
        ...

    def teardown(self) -> None:
        ...

    def spawn(self, preset: Entity) -> int:
        entity_id = self._entity_id_counter
        self._entity_by_id[entity_id] = preset
        self._entity_to_spawn.appendleft(entity_id)
        self._entity_id_counter += 1
        return entity_id

    def kill(self, entity_id: int) -> None:
        self._entity_to_kill(entity_id)

    def update(self, frame_delay: float) -> None:
        self._kill_dead_entities()
        self._spawn_new_entities()

    def get_entity(self, entity_id: int) -> Entity:
        return self._entity_by_id[entity_id]

    def get_entities(self, component_t: Type[COMPONENT_T]) -> Iterable[Entity]:
        return self._entity_by_component_flag.get(component_t, [])

    def get_commands(self, event_type: int) -> Iterable[CommandBinding]:
        return self._command_bindings.get(event_type, [])

    def install(self, event_type: int, command: ICommand, **parameters) -> int:
        binding = CommandBinding(event_type, command, parameters)
        self._command_binding_map[self._command_id_counter] = binding
        self._command_bindings.setdefault(event_type, []).append(binding)
        self._command_id_counter += 1

    def uninstall(self, handle: int) -> None:
        binding = self._command_binding_map.pop(handle)
        self._command_bindings[binding.event_type].remove(binding)

    def _kill_dead_entities(self):
        while self._entity_to_kill:
            entity_id = self._entity_to_kill.pop()
            component_set = self._entity_by_id.pop(entity_id)
            for flag in component_set.keys():
                s = self._entity_by_component_flag[flag]
                s.remove(component_set)

    def _spawn_new_entities(self):
        while self._entity_to_spawn:
            entity_id = self._entity_to_spawn.pop()
            component_set = self._entity_by_id[entity_id]
            for flag in component_set.keys():
                s = self._entity_by_component_flag.setdefault(flag, [])
                s.append(component_set)

    def __init__(self, game: IGame):
        self._game = game

        self._command_id_counter: int = 0
        self._command_bindings: Dict[int, List[CommandBinding]] = dict()
        self._command_binding_map: Dict[int, CommandBinding] = dict()

        self._entity_id_counter: int = 0
        self._entity_by_component_flag: Dict[int, List[Entity]] = dict()
        self._entity_by_id: Dict[int, Entity] = dict()

        self._entity_to_spawn: Deque[int] = deque()
        self._entity_to_kill: Deque[int] = deque()

