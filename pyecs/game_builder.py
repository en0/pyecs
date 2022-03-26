import pygame
from typing import Optional, Type, Callable, Set, Tuple, Any, List
from .typing import IGame, IObjectFactory, ISystemManager, IEntityManager, PROVIDER_T
from .system_manager import SystemManager
from .entity_manager import EntityManagerOpts, EntityManager
from .game import Game

from pyioc3 import StaticContainerBuilder, Container, ScopeEnum
#try:
#except ImportError:
    #StaticContainerBuilder = None
    #Container = None
    #ScopeEnum = None


class ObjectFactory(IObjectFactory):

    _ioc: Container

    def set_ioc(self, ioc: Container) -> None:
        self._ioc = ioc

    def get_provider(self, annotation: Type[PROVIDER_T]) -> PROVIDER_T:
        return self._ioc.get(annotation)



class GameBuilder:

    def using_screen_mode(
        self,
        size: Tuple[int, int] = (0, 0),
        flags: int = 0,
        depth: int = 0,
        display: int = 0,
        vsync: int = 0,
    ) -> None:
        self._assert_not_built()
        self.using_provider(
            lambda:pygame.display.set_mode(size, flags, depth, display, vsync),
            pygame.Surface,
            ScopeEnum.SINGLETON)

    def using_world(self, entities: List, world=None) -> None:
        self._world_entities.append((world, entities))

    def using_component_groups(self, component_groups: Set[int]) -> None:
        opts = EntityManagerOpts(component_groups)
        self.using_constant(EntityManagerOpts, opts)

    def using_system(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        on_activate: Callable[["GameBuilder", PROVIDER_T], PROVIDER_T] = None,
    ) -> None:
        self._assert_not_built()
        anno = annotation or provider
        self._systems.append(anno)
        self.using_provider(provider, anno, ScopeEnum.SINGLETON, on_activate)

    def using_provider(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate: Callable[["GameBuilder", PROVIDER_T], PROVIDER_T] = None,
    ) -> None:
        self._assert_not_built()
        _on_activate = self._wrap_activate(on_activate) if on_activate else None
        self._builder.bind(
            annotation=annotation or provider,
            implementation=provider,
            scope=scope,
            on_activate=_on_activate)

    def using_constant(
        self,
        annotation: Type,
        value: Any,
    ) -> None:
        self._assert_not_built()
        self._builder.bind_constant(annotation, value)

    def build(self) -> IGame:
        self._ensure_built()
        return self._factory.get_provider(IGame)

    def _initialize_system_manager(self, factory: IObjectFactory, sm: ISystemManager):
        for sys_t in self._systems:
            sys = factory.get_provider(sys_t)
            sm.install(sys)
        return sm

    def _initialize_worlds(self, factory: IObjectFactory, em: IEntityManager):
        for world, entities in self._world_entities:
            if world:
                raise NotImplemented()
            else:
                for entity in entities:
                    em.spawn(entity)
        return em

    def _wrap_activate(self, fn):
        def _wrap(impl):
            return fn(self._factory, impl)
        return _wrap

    def _assert_not_built(self):
        if self._ioc is not None:
            raise RuntimeError("Attempt to bind after construction.")

    def _ensure_built(self):
        if self._ioc is None:
            self._ioc = self._builder.build()
            self._factory.set_ioc(self._ioc)

    def _bind_defaults(self):
        self.using_constant(IObjectFactory, self._factory)
        self.using_provider(Game, IGame, ScopeEnum.SINGLETON)
        self.using_provider(
            provider=EntityManager,
            annotation=IEntityManager,
            scope=ScopeEnum.SINGLETON,
            on_activate=self._initialize_worlds)
        self.using_provider(
            provider=SystemManager,
            annotation=ISystemManager,
            scope=ScopeEnum.SINGLETON,
            on_activate=self._initialize_system_manager)

    def __init__(self) -> None:
        if StaticContainerBuilder is None:
            raise RuntimeError("To use the game builder, you must install pyioc3")
        self._factory = ObjectFactory()
        self._builder = StaticContainerBuilder()
        self._ioc: Optional[Container] = None
        self._world_entities = []
        self._systems = []
        self._bind_defaults()

