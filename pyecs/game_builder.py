import pygame
from typing import Optional, Type, Callable, Set, Tuple, Any, List
from pyioc3 import StaticContainerBuilder, Container, ScopeEnum
from .typing import IGame, IObjectFactory, ISystemManager, IEntityManager, PROVIDER_T
from .system_manager import SystemManager
from .entity_manager import EntityManagerOpts, EntityManager
from .game import Game



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
        """Set the pygame display mode"""
        self._assert_not_built()
        self.using_provider(
            lambda:pygame.display.set_mode(size, flags, depth, display, vsync),
            pygame.Surface)

    def using_world_template(self, world: str, entities: List) -> None:
        """Add the given template to the entity manager."""
        self._world_templates[world] = entities

    def using_active_world(self, world: str) -> None:
        """Activate the given world before starting game."""
        self._active_world = world

    def using_component_groups(self, component_groups: Set[int]) -> None:
        """Add component groups to the entity manager.

        Example:
            gamebuilder.using_component_groups([0b1111, 0b1001])

        Arguments:
            component_groups: a set of entity queries.

        """
        opts = EntityManagerOpts(component_groups)
        self.using_constant(EntityManagerOpts, opts)

    def using_clock(self, target_framerate: int) -> None:
        """Install the ClockSystem and ClockService

        Your system can access the ClockService to get the time delta.

        Example:
            class MySystem(ISystem):
                def update(self):
                    print(f"The last frame took {self.clock.frame_delta} seconds.")

                def __init__(self, clock: ClockService):
                    self.clock = clock

            gamebuilder.using_clock(60)

        Arguments:
            target_framerate: The target framerate.
        """
        from .services import ClockService, ClockServiceOpts
        from .systems import ClockSystem
        clock_opts = ClockServiceOpts(framerate=target_framerate)
        self.using_constant(ClockServiceOpts, clock_opts)
        self.using_provider(ClockService)
        self.using_system(ClockSystem)

    def using_system(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        on_activate: Callable[["GameBuilder", PROVIDER_T], PROVIDER_T] = None,
    ) -> None:
        """Add a system to the game.

        Example:

            class MySystem(ISystem):
                def update(self):
                    print("Do something useful")

            gamebuilder.using_system(MySystem)


        Arguments:
            provider: A type that implements the provider.
            annotation: Optional, The annotation used to access the provider.
            on_activate: Optional, A function called with the new instance before
                         it is passed to the dependant.
        """

        self._assert_not_built()
        anno = annotation or provider
        self._systems.append(anno)
        self.using_provider(provider, anno, on_activate=on_activate)

    def using_provider(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        scope: ScopeEnum = ScopeEnum.SINGLETON,
        on_activate: Callable[["GameBuilder", PROVIDER_T], PROVIDER_T] = None,
    ) -> None:
        """Add a provider to the dependecy tree.

        Example:
            class MyInterface(ABC):
                @abstractmethod
                def foo(self): ...

            class MyProvider(MyInterface):
                def foo(self):
                    print("bar")

            gamebuilder.using_provider(
                provider=MyProvider,
                annotation=MyInterface)

        Arguments:
            provider: A type that implements the provider.
            annotation: Optional, The annotation used to access the provider.
            scope: Optional, The scope used when creating an instance of the provider.
            on_activate: Optional, A function called with the new instance before it is
                         passed to the dependant.

        Scopes:
            ScopeEnum.TRANSIENT: Creates a new instance each time the annotation is filled.
            ScopeEnum.REQUESTED: Like transient except the instance is reused if more then
                                 1 provider references this annotation in the same tree.
            ScopeEnum.SINGLETON: will only ever create 1 instance of the provider.
        """
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
        """Add a constant to the dependecy tree.

        This is useful to pass arguments to services. Wrapping them in
        named tuples is a expressive way todo so.

        Example:
            class MyOpts(NamedTuple):
                value1: int

            gamebuilder.using_constant(MyOpts, MyOpts(123))

        Arguments:
            annotation: The annotation used to access the constant
            value: The constant.
        """
        self._assert_not_built()
        self._builder.bind_constant(annotation, value)

    def build(self) -> IGame:
        """Build and return the game object."""
        self._ensure_built()
        return self._factory.get_provider(IGame)

    def play(self) -> None:
        """Build and start playing the game."""
        self.build().play()

    def _initialize_system_manager(self, factory: IObjectFactory, sm: ISystemManager):
        for sys_t in self._systems:
            sys = factory.get_provider(sys_t)
            sm.install(sys)
        return sm

    def _initialize_worlds(self, factory: IObjectFactory, em: IEntityManager):
        for world, entities in self._world_templates.items():
            em.set_world_template(world, entities)
        if self._active_world:
            em.activate_world(self._active_world)
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
        self.using_provider(Game, IGame)
        self.using_provider(
            provider=EntityManager,
            annotation=IEntityManager,
            on_activate=self._initialize_worlds)
        self.using_provider(
            provider=SystemManager,
            annotation=ISystemManager,
            on_activate=self._initialize_system_manager)

    def __init__(self, init: bool = False) -> None:
        """Create a GameBuilder

        Arguments:
            init: If true, the builder will init pygame.
        """
        if init:
            pygame.init()
        self._factory = ObjectFactory()
        self._builder = StaticContainerBuilder()
        self._ioc: Optional[Container] = None
        self._world_templates = {}
        self._active_world = None
        self._systems = []
        self._bind_defaults()

