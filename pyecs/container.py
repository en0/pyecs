from pyioc3 import StaticContainerBuilder, Container, ScopeEnum
from typing import Type, Any, Optional

from .typing import IGameContainer, IScene, ISystem, PROVIDER_T, ActivatorDelegate, IGame


class GameContainer(IGameContainer):

    _builder: StaticContainerBuilder
    _ioc: Optional[Container]

    def add_provider(
        self,
        provider: Type[PROVIDER_T],
        annotation: Type = None,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate: Optional[ActivatorDelegate] = None,
    ) -> None:
        self._assert_not_built()
        self._builder.bind(annotation or provider, provider, scope, on_activate)

    def add_constant(
        self,
        annotation: Type,
        value: Any,
    ) -> None:
        self._assert_not_built()
        self._builder.bind_constant(annotation, value)

    def get_provider(self, provider: Type[PROVIDER_T]) -> PROVIDER_T:
        self._ensure_built()
        return self._ioc.get(provider)

    def _ensure_built(self) -> None:
        if self._ioc is None:
            self._ioc = self._builder.build()

    def _assert_not_built(self) -> None:
        if self._ioc is not None:
            raise RuntimeError("Attempt to bind new provider after container in use.")

    def __init__(self, game: IGame) -> None:
        self._builder = StaticContainerBuilder()
        self._builder.bind_constant(IGame, game)
        self._ioc = None
