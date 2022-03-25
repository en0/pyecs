from typing import Callable
from ..typing import ICommand


class DelegatedCommand(ICommand):

    def execute(self, event) -> None:
        self._delegate(event)

    def __init__(self, delegate: Callable, pass_event: bool = False) -> None:
        self._delegate = delegate if pass_event else (lambda e: delegate())
